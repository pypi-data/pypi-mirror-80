import unittest
import pg_creds
import psycopg2
from examples.load_user_example import load_user_etl

SCHEMA = "testschema"


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


class TestExamples(unittest.TestCase):

    def test_load_user(self):
        stats_expected = {'facts_inserted': 4, 'facts_updated': 0, 'facts_deleted': 0, 'historic_inserted': 0,
                        'historic_updated': 0, 'historic_deleted': 0, 'rows_read': 4, 'rows_parsed': 4}
        stats = load_user_etl()

        stats_parsed = {key: stats[key] for key in stats_expected.keys()}
        self.assertDictEqual(stats_expected, stats_parsed)

    def setUp(self):
        cleanup()

    def tearDown(self):
        cleanup()


if __name__ == '__main__':
    unittest.main()
