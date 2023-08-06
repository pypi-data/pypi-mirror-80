from simpleetl._functions._db_quoting import quote


def _get_nextid(pgconn, schema, table, key):
    q = """SELECT
        coalesce(MAX({key})+1,1) as maxid
        FROM {schema}.{table};""".format(schema=quote(schema, pgconn),
                                         table=quote(table, pgconn),
                                         key=quote(key, pgconn))
    with pgconn.cursor() as cursor:
        cursor.execute(q)
        return cursor.fetchone()[0]
