"""A class for maintaining data warehouse information of batch load, such as
statistics for different processes.
"""
import psycopg2
import time
from simpleetl import CONFIG
from simpleetl._functions._dbfunctions import table_exists


class Batchlog(object):
    """A class describing the properties of one batch load.

    """

    def __init__(self, dsn):
        """Constructor.

        :param batchkey: Optional batchkey, if loading existing batch.
        :param dsn: Connectionstring to database.
        """

        self.__batchkey = None

        self.__schema = "simpleetl"
        self.__table = "batchload"
        self.__db_dsn = dsn
        self.__updated = None
        self.__updated_hist = None
        self.__stats = {"facts_inserted": None,
                        "facts_updated": None,
                        "facts_deleted": None,
                        "historic_inserted": None,
                        "historic_updated": None,
                        "historic_deleted": None,
                        "batch_start": None,
                        "batch_done": None,
                        "batch_secs": None}

        self.__ensure_structure()
        return

    def __ensure_structure(self):
        if not CONFIG.batch_logging_table:
            return
        q = """CREATE SCHEMA IF NOT EXISTS {schema};
                    CREATE TABLE {schema}.{table}
        (
          batchkey serial NOT NULL,
          batch_seconds real,
          rows_read integer,
          rows_parsed integer,
          facts_inserted integer,
          facts_updated integer,
          facts_deleted integer,
          historic_inserted integer,
          historic_updated integer,
          historic_deleted integer,

          batch_start timestamp with time zone,
          wait_start timestamp with time zone,
          processing_start timestamp with time zone,
          prepare_load_start timestamp with time zone,
          migrate_update_done timestamp with time zone,
          migrate_insert_done timestamp with time zone,
          migrate_deleted_done timestamp with time zone,
          batch_done timestamp with time zone,

          dbschema text,
          dbtable text,
          script_path text,
          script_arguments text,

          CONSTRAINT dimbatchload_pkey PRIMARY KEY (batchkey)
        )
        """.format(schema=self.__schema, table=self.__table)
        pgconn = psycopg2.connect(self.__db_dsn, application_name="Simpleetl Batchlog ensure structure")
        with pgconn:
            if not table_exists(pgconn, self.__schema, self.__table):
                with pgconn.cursor() as cursor:
                    cursor.execute(q)
        pgconn.close()

    def new_batch(self, script_path, script_arguments, etlschema, etltable):
        """Creates a new batch for loading data.
        """

        if not CONFIG.batch_logging_table:
            return

        stmt = """INSERT INTO {schema}.{table}
            (script_path, script_arguments, dbschema, dbtable)
            VALUES
            (%s, %s, %s, %s);
            SELECT currval('{schema}.{table}_batchkey_seq') AS id;"""
        pgconn = psycopg2.connect(self.__db_dsn, application_name="Simpleetl Batchlog new_batch")
        with pgconn:
            with pgconn.cursor() as cursor:
                cursor.execute(stmt.format(schema=self.__schema, table=self.__table),
                               (script_path, script_arguments, etlschema, etltable))
                self.__batchkey = cursor.fetchone()[0]
        pgconn.close()
        return

    def get_batchkey(self):
        return self.__batchkey

    def __set_timestamp(self, column):
        """Sets a timestamp for a column to NOW().

        :param column: Column of batch load table to set to NOW().
        """
        if not CONFIG.batch_logging_table:
            return
        stmt = """UPDATE {schema}.{table}
                    SET {column}=NOW() WHERE
                    batchkey={batchkey}"""
        pgconn = psycopg2.connect(self.__db_dsn, application_name="Simpleetl Batchlog set_timestamp")
        with pgconn:
            with pgconn.cursor() as cursor:
                cursor.execute(stmt.format(schema=self.__schema, table=self.__table,
                                           column=column, batchkey=self.__batchkey))
        pgconn.close()

    def __set_value(self, column, value):
        self.__stats[column] = value
        if not CONFIG.batch_logging_table:
            return
        stmt = """UPDATE {schema}.{table}
                            SET {col}={val}
                            WHERE batchkey={batchkey}"""
        pgconn = psycopg2.connect(self.__db_dsn, application_name="Simpleetl Batchlog set_value")
        with  pgconn:
            with pgconn.cursor() as cursor:
                cursor.execute(stmt.format(schema=self.__schema, table=self.__table,
                                           batchkey=self.__batchkey,
                                           col=column,
                                           val=value))

        pgconn.close()

    def set_start(self):
        self.__stats["batch_start"] = time.time()
        self.__set_timestamp("batch_start")

    def set_wait_start(self):
        self.__set_timestamp("wait_start")

    def set_processing_start(self):
        self.__set_timestamp("processing_start")

    def set_prepare_load_start(self):
        self.__set_timestamp("prepare_load_start")

    def set_migrate_update_done(self, rows, histrows):
        self.__set_timestamp("migrate_update_done")
        self.__set_value("facts_updated", rows)
        self.__set_value("historic_updated", histrows)

    def set_migrate_insert_done(self, rows, histrows):
        self.__set_timestamp("migrate_insert_done")
        self.__set_value("facts_inserted", rows)
        self.__set_value("historic_inserted", histrows)

    def set_migrate_removed_done(self, rows, histrows):
        self.__set_timestamp("migrate_deleted_done")
        self.__set_value("facts_deleted", rows)
        self.__set_value("historic_deleted", histrows)

    def set_batch_done(self):
        self.__stats["batch_done"] = time.time()
        self.__stats["batch_secs"] = self.__stats["batch_done"] - self.__stats["batch_start"]
        self.__set_timestamp("batch_done")
        self.__set_value("batch_seconds", "EXTRACT (EPOCH FROM batch_done-batch_start)")

    def set_rows_read(self, rows):
        self.__set_value("rows_read", rows)

    def set_rows_parsed(self, rows):
        self.__set_value("rows_parsed", rows)

    def set_rows_inserted(self, rows):
        self.__set_value("rows_inserted", rows)
    def get_stats(self):
        return self.__stats.copy()
