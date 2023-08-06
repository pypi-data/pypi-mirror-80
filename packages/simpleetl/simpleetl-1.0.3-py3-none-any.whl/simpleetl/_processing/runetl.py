import sys
import time
import traceback

from simpleetl import CONFIG
from simpleetl import LOG
from simpleetl._processing.ETLProcess import ETLProcess

__all__ = ['runETL']


def runETL(facttable, datafeeder,
           db_host,
           db_user, db_pass,
           db_name, db_port,
           data_timestamp=None,
           prefunc=None,
           processfunc=None):
    """ Perform ETL processing.
        :param facttable: Object containing information on Fact Tables.
        :param datafeeder: A data feeder iterator, returning dictionaries.
        :param db_host: Database host.
        :param db_user: Database user.
        :param db_pass: Database pass.
        :param db_name: Database name.
        :param db_port: Optionally, a database port. Defaults to 5432.
        :param data_timestamp: A timestamp defining when a fact is valid. If None, the timestamp for starting ETL will be used.
            This parameter is only used when having history tracking enabled.
        :param prefunc: A "pre-work" function, func(row),that will be executed before splitting data into parallel processing.
            Must return True if rows is valid, otherwise False, which ignores the row.
        :param processfunc: A "parallel-work" function func(row,p_dbcon), that will be executed in parallel, before generic data processing
            If False is returned from function, row will be discarded.
        :return: Dictionary with status data
        """
    t = time.time()
    if CONFIG.debug:
        LOG.info(
            "========== Running ETL in DEBUG mode. Debug messages will be printed and errors not handled ==========")
    e = ETLProcess(facttable, datafeeder,
                   db_host,
                   db_user, db_pass,
                   db_name, db_port,
                   data_timestamp=data_timestamp,
                   prefunc=prefunc,
                   processfunc=processfunc)
    e.lock_tmpfacttable()
    e.ensure_structure()
    try:
        LOG.start_parallel()
        success = e.start_etl()
        if CONFIG.debug: LOG.debug("ETL method completed with status " + str(success))
    except Exception as err:
        tb = traceback.format_exc()
        errmsg = "ETL"

        LOG.error(errmsg, "".join(tb))
        success = False
    if CONFIG.debug: LOG.debug("Stopping logger")

    if success:
        if CONFIG.debug: LOG.debug("Final load")
        e.lock_facttable()
        success = e.final_load()
        e.release_facttable()

    e.release_tmpfacttable()

    LOG.stop_parallel()
    if not success:
        tsstr = time.strftime("%H:%M:%S", time.gmtime(time.time() - t))
        LOG.error("ETL JOB FAILED in " + tsstr)
        if CONFIG.debug: LOG.error("sys.exit(1)")
        sys.exit(1)
    else:
        tsstr = time.strftime("%H:%M:%S", time.gmtime(time.time() - t))
        LOG.info("ETL JOB completed in " + tsstr)
    return e.status()