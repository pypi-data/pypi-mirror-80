import queue
import time
import traceback
from multiprocessing import Process, Lock, Queue, Value

import psycopg2
import pygrametl
from pygrametl import ConnectionWrapper
from pygrametl.tables import BulkFactTable, _quote

from simpleetl import CONFIG
from simpleetl import LOG
from simpleetl._functions._db_tables import generate_bulkloader, getdbfriendlystr


class ETLTransform():
    def __init__(self, facttable, datafeeder, batchlog, data_timestamp, db_dsn, prefunc, processfunc):
        self.__facttable = facttable
        self.__datafeeder = datafeeder
        self.__batchlog = batchlog
        self.__data_timestamp = data_timestamp
        self.__db_dsn = db_dsn
        self.__prefunc = prefunc
        self.__processfunc = processfunc

        self.__procs_started = 0
        self.__procs_done = Value("i", 0)

        self.__lock = Lock()

        # Queue for distributing work loads to background workers
        self.__mp_data_queue = Queue(CONFIG.parallel_processes)
        self.__mp_data_queue.cancel_join_thread()  # Makes sure queue does not make main thread hang if main thread dies

        # Queue enabling background workers to communicate back used partitions to main process.
        self.__mp_partition_queue = None
        if self.__facttable.partitioning_enabled:
            self.__mp_partition_queue = Queue()
            self.__mp_partition_queue.cancel_join_thread()  # Makes sure queue does not make main thread hang if main thread dies

        # Background worker attributes
        self.__bg_worker_id = None
        self.__bg_pygramconn = None
        self.__bg_db_table = None
        self.__bg_partitions_used = None
        self.__bg_partitions_used_hist = None

    def __feeder_handler(self):

        try:
            yield from self.__datafeeder
        except Exception as err:

            tb = traceback.print_exc()
            errmsg = "ETL data feeder exception"

            LOG.error(errmsg, tb)
            self.set_shutdown()

    def __putwait(self, data, timeout=None):
        """
        :param data: Data to put
        :param timeout: Timeout in seconds
        :return:
        """
        tstart = time.time()
        while not self.is_shutdown():

            if timeout and time.time() - tstart > timeout:
                return False
            try:
                self.__mp_data_queue.put(data, timeout=1)
                return True
            except queue.Full:
                continue
        return False

    def start_etl(self):
        # Start up background dimension handlers.
        for dim in self.__facttable.dim_mappings:
            dim.dimension.connect_dim(self.__db_dsn)

        procs = []

        # Start up n background workers.
        LOG.debug("Starting up {n} parallel workers".format(n=CONFIG.parallel_processes))
        for n in range(CONFIG.parallel_processes):
            p = Process(target=self.__etl_bgworker, args=(str(n),))
            p.daemon = True
            p.start()
            procs.append(p)
            self.__procs_started += 1

        nrows = 0
        databatch = []
        t = time.time()
        n = 0
        for n, datarow_raw in enumerate(self.__feeder_handler(), 1):
            datarow = datarow_raw.copy()  # Create a shallow copy to prevent users changing data after being inserted

            if n % CONFIG.print_progress_line == 0:
                LOG.debug("Status " + str(n) + " - " + str(round(time.time() - t)))
            # If we have a prefunc, run it and let output determine if row is valid
            if self.__prefunc is not None:
                op = self.__prefunc(datarow)
                if op == False:
                    continue  # Data shall not be loaded
                elif op != True:
                    LOG.error("Prefunc must return True or False. Got: " + str(op))
                    self.set_shutdown()
                    break

            nrows += 1
            databatch.append(datarow)

            # Data is added in batches of 10000 rows. Communication is expensive.
            if len(databatch) > CONFIG.batch_size:
                if self.is_shutdown():
                    break
                did_insert = False
                while not did_insert:
                    did_insert = self.__putwait(databatch, 1)
                databatch = []
                if self.is_shutdown():
                    break
        self.__batchlog.set_rows_read(n)
        if len(databatch) > 0 and not self.is_shutdown():
            # Add any remaining data to a batch.
            self.__putwait(databatch)
        if not self.is_shutdown():
            tsstr = time.strftime("%H:%M:%S", time.gmtime(time.time() - t))
            LOG.info("All data, " + str(n) + " rows, loaded into workers in " + tsstr)

        # Keep waiting until all batches have been processed
        ends_put = 0
        LOG.debug("Waiting for processes to finish "+str(self.is_shutdown()))
        tstart = time.time()
        while self.__procs_done.value < self.__procs_started and not self.is_shutdown():
            # LOG.debug(str(("ends_put",ends_put,self.__procs_done,self.__procs_started)))
            while ends_put < self.__procs_started:
                success = self.__putwait("END", 300)
                # LOG.debug("putwait test "+str(success))
                if not success:
                    LOG.error(
                        "Background worker not finishing. Queue not getting emptied. " + str(self.__procs_done.value)
                        + " of " + str(self.__procs_started) + " has finished", None)
                    if self.set_shutdown():
                        break
                else:
                    ends_put += 1
            time.sleep(1)
            if time.time() - tstart > 300:
                LOG.error("Background worker not finishing. " + str(self.__procs_done.value)
                          + " of " + str(self.__procs_started) + " has finished", None)
                self.set_shutdown()

        LOG.debug("Cleaning up")
        self.__cleanup_queues()
        if (not self.is_shutdown() and (
                self.__facttable.partitioning_enabled or self.__facttable.partitioning_enabled_hist)):
            while True:
                try:
                    pset, pset_hist = self.__mp_partition_queue.get(timeout=1)
                    for p in pset:
                        self.__facttable.add_used_partition(p)
                    for p in pset_hist:
                        self.__facttable.add_used_partition_hist(p)
                except queue.Empty:
                    break

        if self.is_shutdown():
            LOG.error("Aborting ETL due to error")
            for dim in self.__facttable.dim_mappings:
                if CONFIG.debug: LOG.error("Aboring dimension: " + dim.dimension._get_full_table())
                dim.dimension.abort()
            if CONFIG.debug: LOG.error("Returning from Transform")
            return False

        for dim in self.__facttable.dim_mappings:
            dim.dimension.close()

        tsstr = time.strftime("%H:%M:%S", time.gmtime(time.time() - t))
        LOG.info("All workers done in " + tsstr)
        self.__batchlog.set_rows_parsed(nrows)
        return True

    def __cleanup_queues(self):

        LOG.debug("Emptying and closing data queue")

        while True:
            try:
                self.__mp_data_queue.get_nowait()
            except queue.Empty:
                break

        LOG.debug("Cleanup done")

    def __etl_bgworker(self, worker_id):

        self.__bg_worker_id = worker_id

        self.__bg_partitions_used = set()
        self.__bg_partitions_used_hist = set()
        try:
            while True:

                if self.is_shutdown():
                    break
                try:
                    data = self.__mp_data_queue.get(timeout=1)

                    if data == "END":

                        if self.__bg_pygramconn:
                            self.__bg_pygramconn.commit()
                            self.__bg_pygramconn.close()
                            self.__bg_pygramconn = None
                        break
                    try:
                        status = self.__transform(data)
                        # Status true means everything is okay
                        if isinstance(status, str):
                            tb = traceback.format_exc()
                            LOG.error(status, tb)
                            self.set_shutdown()
                            break
                        elif status == False:
                            break
                    except Exception as err:
                        tb = traceback.format_exc()
                        LOG.error("Background ETL worker failed", tb)
                        self.set_shutdown()

                        break
                except queue.Empty:
                    continue
            if self.__facttable.partitioning_enabled or self.__facttable.partitioning_enabled_hist:
                # Return used partitions to main process, if partitioning is enablefs.
                self.__mp_partition_queue.put((self.__bg_partitions_used, self.__bg_partitions_used_hist))

        except Exception:
            tb = traceback.format_exc()

            LOG.error("Background ETL worker failed", tb)
            self.set_shutdown()
        finally:
            if self.__bg_pygramconn:
                try:
                    self.__bg_pygramconn.rollback()
                    self.__bg_pygramconn.close()
                except Exception:
                    pass
            with self.__lock:
                self.__procs_done.value += 1

    def __transform(self, rows):
        if self.__bg_db_table is None:
            pygrametl.tables.definequote('"')  # Tell pygrametl to quote identifiers.
            name = "SimpleETL BG worker {s}.{t} ({id})".format(s=self.__facttable.schema,
                                                               t=self.__facttable.table,
                                                               id=self.__bg_worker_id)
            pgconn = psycopg2.connect(self.__db_dsn, application_name=name)
            self.__bg_pygramconn = ConnectionWrapper(pgconn)
            keycols = self.__facttable._get_cols(only_lookupatts=True)
            measurecols = self.__facttable._get_cols(include_lookupatts=False, include_ignorecols=True,
                                                     include_changeatts=True)

            self.__bg_db_table = BulkFactTable(name=_quote("tmp_data") + "." +
                                                    _quote(self.__facttable.tmptable),
                                               keyrefs=keycols,
                                               measures=measurecols,
                                               bulkloader=generate_bulkloader(self.__bg_pygramconn),
                                               fieldsep='\t',
                                               rowsep='\n',
                                               nullsubst="\\N",
                                               tempdest=None,
                                               bulksize=100000,
                                               usefilename=False,
                                               dependson=(),
                                               strconverter=getdbfriendlystr)
        n = 0
        """ Variables for accessing facttable object. Variable access is faster than object access"""
        dim_mappings = self.__facttable.dim_mappings
        col_mappings = self.__facttable.simple_mappings
        lookupatts_mappings = self.__facttable._get_cols(only_lookupatts=True)
        marked_deleted = self.__facttable.deleted_rows_method == "mark"
        track_last_updated = self.__facttable.track_last_updated
        track_created = self.__facttable.track_created
        has_processfunc = self.__processfunc is not None
        partitioning_enabled = self.__facttable.partitioning_enabled
        partitioning_enabled_hist = self.__facttable.partitioning_enabled_hist
        factinsert = self.__bg_db_table.insert

        for srcrow in rows:
            n += 1

            destrow = {}
            # If removed rows should be marked, we here add that this row is not deleted.
            # This is necessary, as _deleted is treated as a regular data column and a value is expected.
            if marked_deleted:
                srcrow["_deleted"] = None
            if track_last_updated:
                srcrow["_updated"] = self.__data_timestamp
            if track_created:
                srcrow["_created"] = self.__data_timestamp
            # If any user-defined functionality is provided, execute this first.
            if has_processfunc:
                procoutp = self.__processfunc(srcrow)
                if procoutp is False:
                    continue

            # Looking up values in lookup-only dimensions.
            # This is not inserted but could be used by other dimensions
            for dim in dim_mappings:
                dimkey = dim.dimension.ensure(srcrow, dim.namemapping)
                if dimkey is None:
                    return "No dimension key found for " + str(dim)
                if isinstance(dimkey, tuple):
                    return "Error when handling dimension " + str(dim) + ": " + str(dimkey)
                if dim.insert:
                    destrow[dim.dstcol] = dimkey
                if dim.inject:
                    srcrow[dim.dstcol] = dimkey
            # One-to-one mapping of data from source data to fact column
            for simpcol in col_mappings:
                try:
                    if srcrow[simpcol.srccol] is None:
                        destrow[simpcol.dstcol] = None
                    else:
                        # Add data to destination dictionary, parse by type.
                        destrow[simpcol.dstcol] = simpcol.datatype.parse(srcrow[simpcol.srccol])
                except KeyError as err:
                    return ("Cannot define attribute " + simpcol.dstcol +
                            " - Column " + simpcol.srccol + " missing in source data: " + str(err))
                except Exception as err:
                    return ("Something went bad with " + simpcol.srccol + ". Content: " + str(
                        srcrow[simpcol.srccol]) + ". Error:: " + str(err))
            for lookupcol in lookupatts_mappings:
                if destrow[lookupcol] is None:
                    return ("Column " + lookupcol) + " is part of lookup attributes but value is NULL!"
            # If partition is enabled, add current partition to set of partitions
            if partitioning_enabled:
                p = self.__facttable.get_partition(destrow)
                self.__bg_partitions_used.add(p)
            if partitioning_enabled_hist:
                p = self.__facttable.get_partition_hist(destrow)
                self.__bg_partitions_used_hist.add(p)

            factinsert(destrow)
        return None
