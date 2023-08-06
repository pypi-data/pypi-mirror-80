import calendar
import unittest
from datetime import datetime, date

import psycopg2

import pg_creds
from simpleetl import FactTable, runETL, datatypes, CONFIG

SCHEMA = "testschema"
TABLE = "test_partitioning"
CONFIG.batch_size = 1
CONFIG.parallel_processes = 4
from simpleetl._functions._dbfunctions import get_table_partitions


def datagenerator(rangeadd=0):
    for n in range(24):
        n += rangeadd
        add_years, month = divmod(n, 12)
        month += 1
        year = 2010 + add_years
        yield {"lookupid": n, "datekey": "{y}{m}01".format(y=year, m=str(month).rjust(2, '0'))}


def partitionfunc_yearmonth(value):
    """Function for telling simpleetl to partition facttable by year and month.
    :parameter value: Input is an integer datekey, ex. '2019-11-23' is 20191123
    :return: Tuple with suffix, range_from and range_to, ex. ('201911', 20191101, 20191131)
    """
    dt = datetime.strptime(str(value), "%Y%m%d")
    first_day, last_day = calendar.monthrange(dt.year, dt.month)
    suffix = dt.strftime("%Y_%m")  # 201911
    range_from = int(date(dt.year, dt.month, 1).strftime("%Y%m%d"))  # 20191101, ensures zeropadded month
    range_to = int(date(dt.year, dt.month, last_day).strftime("%Y%m") + str(last_day + 1))  # 20191131
    return suffix, range_from, range_to


def partitionfunc_year(value):
    suffix = str(int(value / 10000))
    range_from = int("{y}0101".format(y=int(value / 10000)))
    range_to = int("{y}0101".format(y=int(value / 10000) + 1))

    return suffix, range_from, range_to


def etlrun(rangeadd):
    f = FactTable(schema=SCHEMA, table=TABLE, lookupatts=["lookupid", "datekey"],
                  store_history=True)
    f.enable_partitioning("datekey", partitionfunc_yearmonth)
    f.enable_partitioning_historic("datekey", partitionfunc_year)
    f.handle_deleted_rows(method="wipe")
    f.add_column_mapping("lookupid", datatypes.bigint)

    f.add_column_mapping("datekey", datatypes.int_notnull)
    stats = runETL(f, datagenerator(rangeadd),
                   db_host=pg_creds.PG_HOST, db_port=pg_creds.PG_PORT,
                   db_name=pg_creds.PG_DBNAME, db_user=pg_creds.PG_USER,
                   db_pass=pg_creds.PG_PASS)
    return stats


def cleanup():
    dsn = ("dbname={dbname} user={username} password={password} host={host} port={port}"
           .format(dbname=pg_creds.PG_DBNAME, username=pg_creds.PG_USER,
                   password=pg_creds.PG_PASS, host=pg_creds.PG_HOST, port=pg_creds.PG_PORT))
    dbcon = psycopg2.connect(dsn)
    with dbcon:
        with dbcon.cursor() as cursor:
            cursor.execute("DROP SCHEMA IF EXISTS " + SCHEMA + " CASCADE")
    dbcon.close()
    print("Cleaned up")


def get_partitions(table):
    dsn = ("dbname={dbname} user={username} password={password} host={host} port={port}"
           .format(dbname=pg_creds.PG_DBNAME, username=pg_creds.PG_USER,
                   password=pg_creds.PG_PASS, host=pg_creds.PG_HOST, port=pg_creds.PG_PORT))
    dbcon = psycopg2.connect(dsn)
    partitions = get_table_partitions(dbcon, SCHEMA, table)
    dbcon.close()
    return partitions


class TestHistoricLoad(unittest.TestCase):

    def test_partitioning(self):
        etlrun(0)
        expected = []
        expected_hist = []
        for y in range(2010, 2012):
            expected_hist.append(TABLE + "_historic_" + str(y))
            for m in range(1, 13):
                expected.append(TABLE + "_" + str(y) + "_" + str(m).rjust(2, '0'))

        test = get_partitions(TABLE)
        self.assertListEqual(test, expected)

        testhist = get_partitions(TABLE + "_historic")
        self.assertListEqual(testhist, expected_hist)

        print("----- NEXT RUN -----")

        # Run next test 12 months  later. This ensures we create and delete partitions
        etlrun(12)

        expected = []
        expected_hist = []
        for y in range(2011, 2013):
            expected_hist.append(TABLE + "_historic_" + str(y))
            for m in range(1, 13):
                expected.append(TABLE + "_historic_" + str(y) + "_" + str(m).rjust(2, '0'))

    def setUp(self):
        cleanup()

    def tearDown(self):
        pass  # cleanup()


if __name__ == '__main__':
    unittest.main()
