import os
import sys
from datetime import datetime
from multiprocessing import Event

import psycopg2
from pygrametl.tables import definequote

from simpleetl import LOG
from simpleetl._functions import _db_schema_handler as schand
from simpleetl._functions._dbfunctions import get_lock, release_lock
from simpleetl._modules.Batchlog import Batchlog
from simpleetl._processing.Postprocess import ETLPostprocess
from simpleetl._processing.Transform import ETLTransform


class ETLProcess(ETLTransform, ETLPostprocess):
    # __manager = Manager()
    __mp_error_event = Event()

    __mainpid = os.getpid()

    def __init__(self,
                 facttable, datafeeder,
                 db_host,
                 db_user, db_pass,
                 db_name, db_port,
                 data_timestamp=None,
                 prefunc=None,
                 processfunc=None):

        self.__facttable = facttable

        self.__db_dsn = ("dbname={dbname} user={username} password={password} host={host} port={port}"
                         .format(dbname=db_name, username=db_user, password=db_pass, host=db_host, port=db_port))
        # If no Type 2 SlowlyChangingFact date is set, use today

        if data_timestamp is None:
            self.__data_timestamp = datetime.utcnow()
        else:
            self.__data_timestamp = data_timestamp

        """ ---------- Initialize ---------- """

        definequote('"')
        self.__mp_error_event.clear()
        self.__batchlog = Batchlog(self.__db_dsn)
        self.__batchlog.new_batch(os.path.abspath(sys.argv[0]), " ".join(sys.argv[1:]),
                                  facttable.schema, facttable.table)
        self.__batchlog.set_start()
        LOG.connect_batchlog(self.__batchlog.get_batchkey())

        ETLTransform.__init__(self, facttable, datafeeder, self.__batchlog, self.__data_timestamp, self.__db_dsn,
                              prefunc, processfunc)
        ETLPostprocess.__init__(self, facttable, self.__batchlog, self.__data_timestamp, self.__db_dsn)

        self.__dbcon_lock = None

    @classmethod
    def set_shutdown(cls):
        cls.__mp_error_event.set()

    @classmethod
    def is_shutdown(cls):
        try:
            os.kill(cls.__mainpid, 0)  # Test if main process is alive. Throws PermissionError if not
        except PermissionError:
            cls.set_shutdown()
            return True
        return cls.__mp_error_event.is_set()

    def lock_tmpfacttable(self):
        if self.__dbcon_lock is None:
            self.__dbcon_lock = psycopg2.connect(self.__db_dsn,
                                                 application_name="Fact table lock" + self.__facttable.schema + "." +
                                                                  self.__facttable.table)
            self.__dbcon_lock.set_session(autocommit=True)
        get_lock(self.__dbcon_lock, self.__facttable.tmptable, False)

    def release_tmpfacttable(self):
        if self.__dbcon_lock is not None:
            release_lock(self.__dbcon_lock, self.__facttable.tmptable)
        self.__dbcon_lock.close()
        self.__dbcon_lock = None

    def lock_facttable(self):
        if self.__dbcon_lock is None:
            self.__dbcon_lock = psycopg2.connect(self.__db_dsn,
                                                 application_name="Fact table lock" + self.__facttable.schema + "." +
                                                                  self.__facttable.table)
            self.__dbcon_lock.set_session(autocommit=True)
        get_lock(self.__dbcon_lock, self.__facttable.schema + "." +
                 self.__facttable.table, False)

    def release_facttable(self):
        if self.__dbcon_lock is not None:
            release_lock(self.__dbcon_lock, self.__facttable.schema + "." + self.__facttable.table)

    def ensure_structure(self):
        # gotlock = dbcon.lock_table(facttable.schema, facttable.table, True)

        # if not gotlock:
        #    LOG.debug("Fact table {s}.{t} is currently utilized by other ETL process. Waiting.."
        #              .format(s=facttable.schema, t=facttable.table))
        #    dbcon.lock_table(facttable.schema, facttable.table, False)

        self.__facttable._validate_structure()
        self.__facttable._prepare_run()

        LOG.info("-------------------- " +
                 "{s}.{t}".format(s=self.__facttable.schema, t=self.__facttable.table) +
                 " --------------------")
        LOG.info("Starting ETL for {s}.{t}".format(s=self.__facttable.schema, t=self.__facttable.table))
        LOG.info("Command: " + " ".join(sys.argv[0:5]) +
                 (len(sys.argv) > 5 and " [more..]" or ""))

        self.__batchlog.set_wait_start()

        pgconn = psycopg2.connect(self.__db_dsn, application_name="Create schema for " +
                                                                  "{s}.{t}".format(s=self.__facttable.schema,
                                                                                   t=self.__facttable.table))

        get_lock(pgconn, "ETL create_schema")
        for dim in self.__facttable.dim_mappings:
            dim.dimension.create_schema(pgconn)

        # Ensure fact table structure

        schand._ensure_structure(pgconn, self.__facttable)
        schand._ensure_indexes(pgconn, self.__facttable)

        # Create table for storing temporary data.

        schand._create_temp_table(pgconn, self.__facttable)

        pgconn.commit()
        release_lock(pgconn, "ETL create_schema")
        pgconn.commit()
        """ ---------- Extract/Transform ---------- """
        pgconn.close()

    def status(self):
        return self.__batchlog.get_stats()
