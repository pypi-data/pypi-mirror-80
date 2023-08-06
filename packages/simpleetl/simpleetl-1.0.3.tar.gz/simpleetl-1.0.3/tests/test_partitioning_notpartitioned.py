import unittest
from simpleetl import FactTable, runETL, datatypes, CONFIG
import pg_creds
import psycopg2

SCHEMA = "testschema"
TABLE = "test_partitioning"
CONFIG.batch_size = 1
CONFIG.parallel_processes = 4
from simpleetl._functions._dbfunctions import table_exists, get_table_partitions

""" Test that ETL can be run, even though table should be partitioned but is not."""


def datagenerator(rangeadd=0):
    for n in range(100):
        n += rangeadd
        add_years, month = divmod(n, 12)
        month += 1
        year = 2010 + add_years
        yield {"lookupid": n, "datekey": "{y}{m}01".format(y=year, m=str(month).rjust(2, '0'))}


def partitionfunc_year(value):
    suffix = str(int(value / 10000))
    range_from = int("{y}0101".format(y=int(value / 10000)))
    range_to = int("{y}0101".format(y=int(value / 10000) + 1))

    return suffix, range_from, range_to


def etlrun(rangeadd, partition=False):
    f = FactTable(schema=SCHEMA, table=TABLE, lookupatts=["lookupid", "datekey"],
                  store_history=True)
    if partition:
        f.enable_partitioning("datekey", partitionfunc_year)
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


def get_partitions():
    dsn = ("dbname={dbname} user={username} password={password} host={host} port={port}"
           .format(dbname=pg_creds.PG_DBNAME, username=pg_creds.PG_USER,
                   password=pg_creds.PG_PASS, host=pg_creds.PG_HOST, port=pg_creds.PG_PORT))
    dbcon = psycopg2.connect(dsn)
    partitions = get_table_partitions(dbcon, SCHEMA, TABLE)
    dbcon.close()
    return partitions


class TestHistoricLoad(unittest.TestCase):

    def test_partitioning(self):
        etlrun(0, False)
        # test = get_partitions()
        # self.assertListEqual(test, [TABLE + "_" + str(y) for y in range(2010, 2019)])

        print(" NEXT RUN ")

        etlrun(0, True)
        # test = get_partitions()
        # self.assertListEqual(test, [TABLE + "_" + str(y) for y in range(2014, 2023)])

    def setUp(self):
        cleanup()

    def tearDown(self):
        cleanup()


if __name__ == '__main__':
    unittest.main()
