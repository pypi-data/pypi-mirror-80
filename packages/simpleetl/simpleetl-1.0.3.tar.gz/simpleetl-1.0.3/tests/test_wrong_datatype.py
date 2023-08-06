import unittest
from simpleetl import FactTable, runETL, datatypes, CONFIG
import pg_creds
import psycopg2

SCHEMA = "testschema"


def datagenerator(return_string):
    for n in range(10):
        if return_string:
            intstr = str(n * 1000)
        else:
            intstr = n * 1000
        yield {"lookupid": n, "teststr": intstr}


def etlrun(use_string):
    f = FactTable(schema=SCHEMA, table="test_wrong_datatype", lookupatts=["lookupid"])
    f.add_column_mapping("lookupid", datatypes.bigint)
    if use_string:
        f.add_column_mapping("teststr", datatypes.text)
    else:
        f.add_column_mapping("teststr", datatypes.int)
    runETL(f, datagenerator(use_string),
           db_host=pg_creds.PG_HOST, db_port=pg_creds.PG_PORT,
           db_name=pg_creds.PG_DBNAME, db_user=pg_creds.PG_USER,
           db_pass=pg_creds.PG_PASS)


class TestWrongDatatypes(unittest.TestCase):

    def test_facttable(self):
        etlrun(False)
        with self.assertRaises(SystemExit):
            etlrun(True)


    def tearDown(self):
        dsn = ("dbname={dbname} user={username} password={password} host={host} port={port}"
               .format(dbname=pg_creds.PG_DBNAME, username=pg_creds.PG_USER,
                       password=pg_creds.PG_PASS, host=pg_creds.PG_HOST, port=pg_creds.PG_PORT))
        dbcon = psycopg2.connect(dsn)
        with dbcon:
            with dbcon.cursor() as cursor:
                cursor.execute("DROP SCHEMA IF EXISTS " + SCHEMA + " CASCADE")
        dbcon.close()
        print("Cleaned up")


if __name__ == '__main__':
    unittest.main()
