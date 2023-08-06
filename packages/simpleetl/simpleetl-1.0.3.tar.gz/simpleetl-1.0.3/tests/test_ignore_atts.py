import unittest
from simpleetl import FactTable, runETL, datatypes, CONFIG
import pg_creds
import psycopg2

SCHEMA = "testschema"
TABLE = "test_historic_load"


def datagenerator(run_no):
    for n in range(100):
        changestr = str(n * 1000 * run_no)
        yield {"lookupid": n, "teststr": changestr}


def etlrun(run_no):
    f = FactTable(schema=SCHEMA, table=TABLE, lookupatts=["lookupid"], ignore_atts=["teststr"],
                  store_history=True)
    f.handle_deleted_rows(method="wipe")
    f.add_column_mapping("lookupid", datatypes.bigint)

    f.add_column_mapping("teststr", datatypes.text)
    stats = runETL(f, datagenerator(run_no),
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


class TestHistoricLoad(unittest.TestCase):

    def test_historicload(self):
        stats1_output = {'facts_inserted': 100, 'facts_updated': 0, 'facts_deleted': 0, 'historic_inserted': 100,
                         'historic_updated': 0, 'historic_deleted': 0,
                         'rows_read': 100, 'rows_parsed': 100}
        stats2_output = {'facts_inserted': 0, 'facts_updated': 0, 'facts_deleted': 0, 'historic_inserted': 0,
                         'historic_updated': 0, 'historic_deleted': 0,
                         'rows_read': 100, 'rows_parsed': 100}


        stats1 = etlrun(1)
        stats1_parsed = {key: stats1[key] for key in stats1_output.keys()}
        self.assertDictEqual(stats1_output, stats1_parsed)

        stats2 = etlrun(2)
        stats2_parsed = {key: stats2[key] for key in stats2_output.keys()}
        self.assertDictEqual(stats2_output, stats2_parsed)

    def setUp(self):
        cleanup()

    def tearDown(self):
        cleanup()


if __name__ == '__main__':
    unittest.main()
