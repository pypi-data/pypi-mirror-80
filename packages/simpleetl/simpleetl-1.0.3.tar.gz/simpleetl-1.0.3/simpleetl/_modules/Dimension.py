import os
import queue
import sys
import traceback
from collections import namedtuple
from functools import lru_cache
from multiprocessing import Process, Queue, Lock

import psycopg2
from pygrametl import getvalue, ConnectionWrapper
from pygrametl.tables import CachedDimension

from simpleetl import LOG, CONFIG
from simpleetl._functions import _datatypes
from simpleetl._functions._db_quoting import quote, quotelist
from simpleetl._functions._db_schema_handler import addcol
from simpleetl._functions._dbfunctions import table_exists, has_index, get_lock_transaction
from simpleetl._processing.ETLProcess import ETLProcess

# Data structure for mapping field between raw data and
# table column, including data type
Column = namedtuple("Column", ["srccol", "dstcol", "datatype"])

# Data structure for mapping a source data field to a dimension
# dimension is dimension object, dstcol is destination column in fact table,
# namemapping is a mapping {dstname: sourcename} where dstname is a column name used by the
# dimension object and sourcename is the name from the data source.
# Inject defines if the found key value from the dimension will be injected into the source data, e.g., to be used
# by other dimensions.
DimColumn = namedtuple("DimColumn", ["dimension", "dstcol", "namemapping", "inject", "insert", "fkey", "allow_null"])

# Dictionaries are ordered by creation by default from python 3.6
dict_ordered = (sys.version_info.major == 3 and sys.version_info.minor >= 6)


def _quote(schema, table): return '"' + schema + '"."' + table + '"'


class Dimension:
    """Dimension object
    """

    def __init__(self, schema, table, key, rowexpander=None,
                 cachesize=100000, integerkey=False):
        """
        :param schema: Schema for dimension.
        :param table: Table for dimension.
        :param key: Primary key of table.
        :param rowexpander: Rowexpander functionality for expanding data to. Must be dict
        :param cachesize: Size of cache.
        :param integerkey: Use integer instead of (default) bigint,
        """

        self.__schema = schema
        self.__table = table
        self.__key = key
        self.__rowexpander = rowexpander
        self.__cachesize = cachesize
        self.__mainpid = os.getpid()

        if integerkey == True:
            self.__keytype = _datatypes.int_notnull

        else:
            self.__keytype = _datatypes.bigint_notnull

        self.__atts = []
        self.__lookupatts = []
        self.__proc = None

        self.__dim = None

        self.__qin = Queue(100)
        self.__qin.cancel_join_thread()  # Makes sure queue does not make main thread hang if main thread dies
        self.__qout = Queue(100)
        self.__qout.cancel_join_thread()  # Makes sure queue does not make main thread hang if main thread dies
        self.__lock = Lock()

        self.__hits = 0
        self.__bghits = 0

        self.__pygramconn = None
        self.__pgconn = None

    def add_lookupatt(self, name, dtype, default_value=chr(0)):
        """
        Add lookup attribute for dimension
        :param name: Name of destination column
        :param dtype: Datatype
        :param default_value: Allow substitution with this value when missing.
            If NULL CHR (chr(0)), do not allow missing values
        :return:
        """
        if dtype.allow_null:
            dtype = dtype.copy(False)  # Ensure we disallow NULL
        if name == self.__key:
            # If we use a smart key, i.e. user-defined primary key, update the datatype according.
            self.__keytype = dtype
        self.__lookupatts.append((name, dtype, default_value))

    def get_lookupatts(self):
        return self.__lookupatts.copy()

    def add_att(self, name, dtype, default_value=chr(0)):
        self.__atts.append((name, dtype, default_value))

    def get_lookuptype(self, name):
        for lname, ltype, defval in self.__lookupatts:
            if lname == name:
                return ltype
        raise ValueError("Dimension.get_lookuptype (" + self.__schema + "." + self.__table +
                         "): Did not find name " + name + " in " + str(self.__lookupatts))

    def connect_dim(self, db_dsn, errorqueue=None):
        # If we only have one lookup att and it is the same as the key, we have a
        # smart key. Thus we do not need to need to wait for return values from the
        # dimension but we can compute this ourselves.
        """
        :param db_dsn: Database connectionstring
        :param errorqueue: Message queue to tell main process if any errors happens.
        :return:
        """
        if len(self.__lookupatts) == 0:
            raise AttributeError("No lookup atts added to dimension " + self._get_full_table())

        if errorqueue is None:
            class custq:
                def __init__(self):
                    pass

                def put(self, data):
                    print(data)

            errorqueue = custq()
        self.__db_dsn = db_dsn
        self.__errorqueue = errorqueue

        if self.__proc is None:
            self.__proc = Process(target=self.__bgworker)
            self.__proc.daemon = True
            self.__proc.start()

    def _get_schema(self):
        return self.__schema

    def _get_table(self):
        return self.__table

    def _get_full_table(self):
        return _quote(self.__schema, self.__table)

    def _get_key(self):
        return self.__key

    def _get_keytype(self):

        return self.__keytype

    def create_schema(self, pgconn):
        if len(self.__lookupatts) == 0:
            raise AttributeError("No lookup atts added to dimension " + self._get_full_table())
        # Backward compatibility, when dsn was given instead of pgconn
        close_pgconn = False
        if isinstance(pgconn, str):
            pgconn = psycopg2.connect(pgconn, application_name="Dim ensure: " + self._get_full_table())
            close_pgconn = True

        if not table_exists(pgconn, self.__schema, self.__table):
            tabcreate = """CREATE SCHEMA if not exists {sch};
                CREATE TABLE if not exists {sch}.{tab}
                (  {key} {keytype},
                   PRIMARY KEY ({key}))
            """.format(sch=quote(self.__schema, pgconn), tab=quote(self.__table, pgconn), key=quote(self.__key, pgconn),
                       keytype=self.__keytype.sqltype())
            with pgconn.cursor() as cursor:
                cursor.execute(tabcreate)

        uniqueidx = []

        for col, datatype, _ in self.__lookupatts:
            uniqueidx.append(col)
            # self.__addcol(pgconn, col, datatype)
            addcol(self.__schema, self.__table, pgconn, col, datatype)
        for col, datatype, _ in self.__atts:
            # self.__addcol(pgconn, col, datatype, True)
            addcol(self.__schema, self.__table, pgconn, col, datatype)
        lookupidx = uniqueidx.copy()
        lookupidx.append(self.__key)

        hasidx = has_index(pgconn, self.__schema, self.__table, lookupidx)
        if not hasidx:
            idx = """CREATE unique INDEX ON {schema}.{table}
                                        ({keycols});
                                        """.format(schema=quote(self.__schema, pgconn),
                                                   table=quote(self.__table, pgconn),
                                                   keycols=", ".join(quotelist(lookupidx, pgconn)))

            with pgconn.cursor() as cursor:
                cursor.execute(idx)
        from simpleetl._functions._dbfunctions import has_unique, create_unique
        if not has_unique(pgconn, self.__schema, self.__table, uniqueidx):
            create_unique(pgconn, self.__schema, self.__table, uniqueidx)
        pgconn.commit()
        if close_pgconn:
            pgconn.close()

    def close(self):
        if self.__proc is not None:
            self.__qin.put("STOP")
            h, bgh = self.__qout.get(timeout=5)
            self.__proc.join()
        self.__proc = None

    def abort(self):
        if self.__proc is not None:
            self.__qin.put("ABORT")
            self.__proc.join()

            self.__hits = 0
            self.__bghits = 0
            self.__proc = None

    """ ---------- The following methods are methods run by parallel background worker ETL processes ---------- """

    def ensure(self, srcdata, namemapping={}):
        """
        Ensure a dimension attribute exists and return key.
        :param srcdata:
        :param namemapping:
        :return:
        """

        # Start up background worker, in case not started
        if not self.__proc:
            LOG.error(
                "Ensure called on dimension, but dimension has not been connected yet: " + self.__schema + "." + self.__table)

        # Construct a lookup row for the dimension, given the lookup attributes.
        dimrow = {}

        for colname, datatype, default_value in self.__lookupatts:
            try:
                k = getvalue(srcdata, colname, namemapping)
            except KeyError as err:
                errstr = (
                        "Dimension " + self._get_full_table() + " requires lookup attribute " + colname + ". This was not found in source data: " + str(
                    srcdata.keys()))
                LOG.error(errstr)
                # raise KeyError("dimension line ~124: " + self.get_full_table() + " ensure error: " + str(err))
                return ((errstr, err))

            if k is None:
                if default_value is not chr(0):
                    k = default_value
                else:
                    errstr = (
                            "Lookup-attribute is None in dimension for lookup-attribute" + colname + " in " + self._get_full_table() + ". Value '" + str(
                        k) + "' parsed to 'None'")
                    LOG.error(errstr)
                    return ((errstr, None))
            try:
                outval = datatype.parse(k)
            except AttributeError as err:
                errstr = (
                        "Lookup-attribute is wrong type in dimension for lookup-attribute" + colname + " in " + self._get_full_table() + ". Value '" + str(
                    k) + "' parsed to 'None'. Error: " + str(err))
                LOG.error(errstr)
                return ((errstr, err))

            if outval is None:
                errstr = (
                        "Could not parse dimensioon lookup-attribute" + colname + " in " + self._get_full_table() + ". Value '" + str(
                    k) + "' parsed to '" + str(outval) + "'")
                LOG.error(errstr)
                return ((errstr, None))

            dimrow[colname] = outval

        self.__hits += 1
        for colname, datatype, default_value in self.__atts:
            try:
                k = getvalue(srcdata, colname, namemapping)
            except KeyError as err:
                if default_value is not chr(0):
                    k = default_value
                else:
                    continue

            if k is None:
                if default_value is not chr(0):
                    k = default_value
                else:
                    continue
            outval = datatype.parse(k)
            if outval is None:
                errstr = (
                        "Could not parse dimension attribute " + colname + " in " + self._get_full_table() + ". Value '" + str(
                    k) + "' parsed to '" + str(outval) + "'")
                LOG.error(errstr)
                return (errstr, None)
            dimrow[colname] = outval

        # Create a frozen set, which can be cached, from the input dictionary
        dimrow = frozenset(dimrow.items())
        return self.__decoupled_return_ensure(dimrow)

    @lru_cache(100000)
    def __decoupled_return_ensure(self, data):
        """
        :param datamsg:
        :param row: Input data, can be either a message, "STOP" or "ABORT", or a frozenset of data to look up.
        :return: Dimension key returned from background worker
        """
        with self.__lock:
            self.__qin.put(data)
            return self.__qout.get()

    """ ---------- The following methods are background worker methods ---------- """

    def __bgworker(self):
        """
        Background worker, handling dimension database action.
        """
        self.__connect_bgworker()
        abort = False

        while True:
            try:
                # Get entry from queue. Wait up to three seconds, before testing if something is wrong
                data = self.__qin.get(timeout=3)
            except queue.Empty:
                try:
                    os.kill(self.__mainpid, 0)  # Test if main process is alive. Throws PermissionError if not
                    if ETLProcess.is_shutdown():
                        data = "ABORT"
                    else:
                        continue
                except PermissionError:
                    # Main process is dead
                    data = "ABORT"

            if data == "STOP":
                break
            elif data == "ABORT":
                abort = True
                break
            else:
                self.__hits += 1
                v = self.__do_map(data)
                self.__qout.put(v)

        if not CONFIG.simulate and not abort:
            self.__pygramconn.commit()
        else:
            self.__pygramconn.rollback()
        self.__pygramconn.close()

        self.__qout.put((self.__hits, self.__bghits))

    def __connect_bgworker(self):
        self.__pgconn = psycopg2.connect(self.__db_dsn, application_name="SimpleETL Dimension {s}.{t}".format(
            s=self.__schema, t=self.__table))
        self.__pygramconn = ConnectionWrapper(self.__pgconn)

        atts = [a[0] for a in self.__lookupatts + self.__atts]
        if self.__key in atts:
            atts.remove(self.__key)

        def _getnextid(ignoredrow, ignoredmapping):
            """
            Function for always fetching greatest ID from DB table. This enables parallel ETL as multiple dimension
            objects on the same table can run in parallel.
            :param ignoredrow:
            :param ignoredmapping:
            :return:
            """
            with self.__pygramconn.cursor() as cursor:
                cursor.execute("SELECT coalesce(MAX({id}),0)+1 as id FROM {t}".format(id=self.__key,
                                                                                      t=self._get_full_table()))
                row = cursor.fetchone()
            return row[0]

        self.__dim = CachedDimension(name=self._get_full_table(),
                                     key=self.__key,
                                     lookupatts=[a[0] for a in self.__lookupatts],
                                     attributes=atts,
                                     size=self.__cachesize,
                                     usefetchfirst=True,
                                     prefill=True,
                                     idfinder=_getnextid,
                                     cacheoninsert=False,  # Very important, this enforces to look in the DB for data.
                                     rowexpander=self.__rowexpander,
                                     targetconnection=self.__pygramconn)
        self.__pygramconn.commit()

    @lru_cache(10000)
    def __do_map(self, inputrow):
        try:
            row = dict(inputrow)
            keyval = self.__dim.lookup(row)
            if keyval is None:
                lockkey = self.__schema + "." + self.__table
                self.__bghits += 1
                # Require a transaction lock on the dimension table. This ensures other ETL processes can use the same
                # dimension in parallel, but inserted entries will immediately be available to other ETL processes.
                # Lock is released upron commit or rollback.
                get_lock_transaction(self.__pgconn, lockkey)

                keyval = self.__dim.ensure(row)
                if not CONFIG.simulate:
                    # Other seperate ETL jobs can utilized the same dimension. Therefore we need to commit changes immediately to the DB
                    self.__pygramconn.commit()
                else:
                    self.__pygramconn.rollback()

        except:
            err = sys.exc_info()[0]
            keyval = ("Error", str(err) + " - " + str(traceback.print_exc()))

        return keyval
