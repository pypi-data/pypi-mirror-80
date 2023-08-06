from datetime import datetime

from simpleetl import LOG
from simpleetl import CONFIG
from simpleetl import FactTable
from simpleetl import datatypes as dt
from simpleetl import runETL
from examples.datedimension_example import dimdate
from examples.timedimension_example import dimtime
import pg_creds


def data_generator():
    """ Simple data generator, yielding dictionaries of data.
    Could as well be a file parser or anything else
    :return:
    """
    userdata = [{"userid": 42, "sys_username": "Jens",
                 "created": datetime.strptime("2019-02-26 07:32:15", "%Y-%m-%d %H:%M:%S")},
                {"userid": 56, "sys_username": "Svend",
                 "created": datetime.strptime("2019-04-11 12:54:11", "%Y-%m-%d %H:%M:%S")},
                {"userid": 78, "sys_username": "Niels",
                 "created": datetime.strptime("2019-07-21 07:12:52", "%Y-%m-%d %H:%M:%S")},
                 {"userid": 23, "sys_username": "Poul",
                  "created": datetime.strptime("2019-07-21 07:10:52", "%Y-%m-%d %H:%M:%S")
                  }
                ]
    for user in userdata:
        yield user



def processrow(row):
    """ Function for transforming each single row.
    :param row: Input data row as dictionary. Data transformations must be updated in this dictionary,
        e.g., row["name_lower"] = row["name"].lower()
    :return: Can return True or None if row is fine. If function returns false, row will be discarded and not inserted.
    """
    if row["created"] is None:
        # If we have no created timestamp, row is invalid and we discard it
        return False

    row["created_datekey"] = int(row["created"].strftime("%Y%m%d"))
    # The date dimension expects a datekey smart key as integer

    row["created_timekey"] = int(row["created"].strftime("%H%M"))
    # The time dimension expects a timekey smart key as integer


def load_user_etl():
    LOG.info("Starting to define ETL")
    p = FactTable(schema="testschema", table="userdata",
                  migrate_updates=True,
                  # Updated to data will be processed. Can be set to False if only appending (will speed things up)
                  store_history=False,  # Create a seperate userdata_historic table for storing changes to facts.
                  track_last_updated=True,
                  # Adds an _updated attribute which keeps track of when data was last updated.
                  lookupatts=["userid"]  # List of attributes uniquely defining a fact
                  )

    p.handle_deleted_rows("mark")
    # Tells ETL to mark deleted rows from source with an _deleted timestamp attribute

    p.add_column_mapping("userid", dt.bigint, "userid")
    # Map userid from source data to database with same name

    p.add_column_mapping("sys_username", dt.text, "username")
    # Rename "sys_username" from source data to "username" in database

    p.add_column_mapping("created", dt.timestamp, "created_timestamp")
    # Remap "created" in source data to "created_timestamp" in database

    p.add_dim_mapping(dimdate, "created_datekey", {"datekey": "created_datekey"})
    # dimdate expects a datekey, hence we create a namemapping from created_datekey to datekey is created

    p.add_dim_mapping(dimtime, "created_timekey", {"timekey": "created_timekey"})
    # dimtime expects a timekey attribyte, hence a namemapping from created_timekey to timekey is created

    datafeeder = data_generator()
    # datafeeder is our data generator object
    #

    CONFIG.print_progress_line = 1
    # Make simpleETL print progress for every n lines

    CONFIG.debug = False
    # Enabled debugging of ETL. Will not drop temporary and will print SQLs for easier debugging.

    # CONFIG.simulate = False # Can simulate effects of ETL run
    # CONFIG.batch_size = 1000 Batch size of rows being distributed for each parallel worker
    # CONFIG.parallel_processes = multiprocessing.cpu_count() #Increase or decrease number of parallel bach workers.
    # CONFIG.batch_logging_table = True # Simpleetl will log batchload metadata to simpleetl.batchload table

    LOG.info("Executing ETL process")
    stats = runETL(facttable=p,
                   datafeeder=datafeeder,
                   prefunc=None,
                   # A function for each row running in the main thread can be defined. Can be usefull,
                   # e.g., if it is required to compare data globaly to detect duplicates.
                   processfunc=processrow,  # Each row must be processed by this function in each worker.
                   db_host=pg_creds.PG_HOST, db_port=pg_creds.PG_PORT,
                   db_name=pg_creds.PG_DBNAME, db_user=pg_creds.PG_USER,
                   db_pass=pg_creds.PG_PASS)
    print(stats)
    return stats

if __name__ == "__main__":
    load_user_etl()
