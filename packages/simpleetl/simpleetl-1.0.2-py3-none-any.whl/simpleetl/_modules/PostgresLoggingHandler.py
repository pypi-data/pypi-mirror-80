import logging
import psycopg2


## Logging handler for PostgreSQL
#
#
class pgLogHandler(logging.Handler):
    __schema = "simpleetl"
    __table = "log"
    initial_sql = """CREATE SCHEMA IF NOT EXISTS {schema};
                    CREATE TABLE IF NOT EXISTS {schema}.{table}(
                    logid bigserial,
                        logtime timestamp with time zone DEFAULT NOW(),
                        batchkey int,
                        created text,
                        name text,
                        loglevel int,
                        loglevelname text,
                        message text,
                        args text,
                        module text,
                        funcname text,
                        lineno int,
                        exception text,
                        process int,
                        thread text,
                        threadname text
                   )""".format(schema=__schema, table=__table)

    insertion_sql = """INSERT INTO {schema}.{table}(
                            batchkey,
                            created,
                            name,
                            loglevel,
                            loglevelname,
                            message,
                            module,
                            funcname,
                            lineno,
                            exception,
                            process,
                            thread,
                            threadname) VALUES (
                            %(batchkey)s,
                            %(created)s,
                            %(name)s,
                            %(levelno)s,
                            %(levelname)s,
                            %(msg)s,
                            %(module)s,
                            %(funcName)s,
                            %(lineno)s,
                            %(exc_text)s,
                            %(process)s,
                            %(thread)s,
                            %(threadName)s
                    )""".format(schema=__schema, table=__table)

    def connect(self, db_host, db_name, db_user, db_pass, db_port):

        try:

            self.__connect = psycopg2.connect(
                database=db_name,
                host=db_host,
                user=db_user,
                password=db_pass,
                port=db_port)
            self.__connect.autocommit = True

            return True
        except:
            return False

    def __init__(self, lbatchkey, db_host, db_name, db_user, db_pass, db_port):

        self.__batchkey = -1

        self.__connect = None

        if not self.connect(db_host, db_name, db_user, db_pass, db_port):
            print("Database connection error, no logging")
            return

        logging.Handler.__init__(self)

        self.__connect.cursor().execute(pgLogHandler.initial_sql)
        self.__connect.commit()
        self.__connect.cursor().close()

    def connect_batch(self, batchkey):
        self.__batchkey = batchkey

    def emit(self, record):

        # Use default formatting:
        self.format(record)

        if record.exc_info:
            record.exc_text = logging._defaultFormatter.formatException(record.exc_info)
        else:
            record.exc_text = ""
        recdict = record.__dict__
        recdict["batchkey"] = self.__batchkey

        try:
            cur = self.__connect.cursor()
        except:
            self.connect()
            cur = self.__connect.cursor()

        cur.execute(pgLogHandler.insertion_sql, recdict)
        self.__connect.commit()
        self.__connect.cursor().close()
