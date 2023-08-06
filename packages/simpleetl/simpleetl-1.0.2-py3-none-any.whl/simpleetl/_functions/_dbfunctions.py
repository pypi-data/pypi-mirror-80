import hashlib
from functools import lru_cache

from psycopg2.extensions import quote_ident


def table_exists(pgconn, schema, table):
    """ Returns true, if table exists in data warehouse.
    :param pgconn: Psycopg2 connection
    :param schema: Schema name.
    :param table: Table name.
    :return: True if table exists, else False.
    """

    stmt = "SELECT COUNT(1) AS n FROM pg_tables WHERE tablename=%s AND schemaname=%s"
    with pgconn.cursor() as cursor:
        cursor.execute(stmt, [table, schema])
        return cursor.fetchone()[0] == 1


def has_index(pgconn, schema, table, cols):
    cols2 = cols.copy()
    for col in cols:
        cols2.append(quote_ident(col, pgconn))
    q = """with idxs as (SELECT i.relname as indname,
       i.relowner as indowner,
       idx.indrelid::regclass,
       am.amname as indam,
       idx.indkey,
       ARRAY(
       SELECT replace(replace(pg_get_indexdef(idx.indexrelid, k + 1, true),'"',''),'\\','')
       FROM generate_subscripts(idx.indkey, 1) as k
       ORDER BY k
       ) as indkey_names,
       idx.indexprs IS NOT NULL as indexprs,
       idx.indpred IS NOT NULL as indpred
FROM   pg_index as idx
JOIN   pg_class as i
ON     i.oid = idx.indexrelid
JOIN   pg_am as am
ON     i.relam = am.oid
where idx.indrelid::regclass ='{schema}.{table}'::regclass)
select * from idxs
    where indkey_names = %s
--
    """.format(schema=quote_ident(schema, pgconn),
               table=quote_ident(table, pgconn))
    with pgconn.cursor() as cursor:
        cursor.execute(q, (cols,))

    return cursor.rowcount > 0


def column_exists(pgconn, schema, table, column):
    """ Returns true, if column in table exists in data warehouse.
    :param pgconn: psycopg2 connection.
    :param schema: Schema name.
    :param table: Table name.
    :param column: Table column
    :return: True if table exists, else False.
    """

    sql = """
    SELECT
        COUNT(1) AS n
    FROM information_schema.columns
    WHERE table_schema = %s
        AND table_name = %s
        AND column_name = %s;
        """
    with pgconn.cursor() as cursor:
        cursor.execute(sql, (schema, table, column))
        tablecount = cursor.fetchone()
    return tablecount[0] == 1


def column_type(pgconn, schema, table, column):
    """ Returns datatype, if column in table exists, otherwise returns None.
        :param pgconn: psycopg2 connection.
        :param schema: Schema name.
        :param table: Table name.
        :param column: Table column
        :return: Column if exists, otherwise None.
        """

    q_ddl = """	SELECT udt_name::regtype as datatype,
                is_nullable,
                numeric_precision,
                numeric_scale
            FROM INFORMATION_SCHEMA.COLUMNS WHERE table_schema=%s 
            AND table_name=%s
            AND column_name=%s
            """
    with pgconn.cursor() as cursor:
        cursor.execute(q_ddl, (schema, table, column))

        if cursor.rowcount == 0:
            return None
        col = cursor.fetchone()

    data_type = col[0]
    is_nullable = col[1]
    numeric_precision = col[2]
    numeric_scale = col[3]

    if data_type == "numeric":
        data_type += "({p},{s})".format(p=numeric_precision, s=numeric_scale)
    if is_nullable == "NO":
        data_type += " NOT NULL"
    return data_type


def has_fkey(pgconn, srcschema, srctable, srccol, dstschema, dsttable, dstcol):
    q = """select 1
    from pg_attribute af, pg_attribute a,
      (select conrelid,confrelid,conkey[i] as conkey, confkey[i] as confkey
       from (select conrelid,confrelid,conkey,confkey,
                    generate_series(1,array_upper(conkey,1)) as i
             from pg_constraint where contype = 'f') ss) ss2
    where af.attnum = confkey and af.attrelid = confrelid and
          a.attnum = conkey and a.attrelid = conrelid

          and confrelid::regclass='{dstschema}.{dsttable}'::regclass
          and af.attname ='{dstcol}'
          and conrelid::regclass = '{srcschema}.{srctable}'::regclass
          and a.attname ='{srccol}'
          --and replace(confrelid::regclass::text,'"','')=replace('{dsttable}','"','')
          --and replace(af.attname,'"','') =replace('{dstcol}','"','')
          --and replace(conrelid::regclass::text,'"','') = replace('{srctable}','"','')
          --and replace(a.attname,'"','') =replace('{srccol}','"','')
    """.format(srcschema=quote_ident(srcschema, pgconn),
               srctable=quote_ident(srctable, pgconn),
               srccol=srccol,
               dstschema=quote_ident(dstschema, pgconn),
               dsttable=quote_ident(dsttable, pgconn),
               dstcol=dstcol)
    with pgconn.cursor() as cursor:
        cursor.execute(q)

    return cursor.rowcount > 0


def has_unique(pgconn, schema, table, cols):
    q = """select
    b.relname as table,
    a.conname as constraint,
    array_agg(c.attname) as const_columns
from pg_constraint a, pg_class b, pg_attribute c
where
	contype='u' and 
 conrelid::regclass=%s::regclass
    and a.conrelid = b.oid
    and c.attrelid = b.oid
    and c.attnum in (select unnest(a.conkey))
group by b.relname, a.conname"""

    with pgconn.cursor() as cursor:
        cursor.execute(q, (schema + "." + table,))
        const = cursor.fetchall()

    for c in const:
        constlist = c[2]
        if set(constlist) == set(cols):
            return True
    return False


def create_unique(pgconn, schema, table, cols):
    q = """ALTER TABLE {schema}.{table} ADD UNIQUE ({cols})
    """.format(schema=quote_ident(schema, pgconn),
               table=quote_ident(table, pgconn),
               cols=", ".join([quote_ident(c, pgconn) for c in cols]))
    with pgconn.cursor() as cursor:
        cursor.execute(q)


def create_fkey(pgconn, srcschema, srctable, srccol, dstschema, dsttable, dstcol, deferrable=False):
    defer = ""
    if deferrable:
        defer = "deferrable initially deferred"
    q = """alter table {srcschema}.{srctable} add foreign key ({srccol}) references {dstschema}.{dsttable} ({dstcol}) {defer}
    """.format(srcschema=quote_ident(srcschema, pgconn),
               srctable=quote_ident(srctable, pgconn),
               srccol=quote_ident(srccol, pgconn),
               dstschema=quote_ident(dstschema, pgconn),
               dsttable=quote_ident(dsttable, pgconn),
               dstcol=quote_ident(dstcol, pgconn),
               defer=defer)
    with pgconn.cursor() as cursor:
        cursor.execute(q)


@lru_cache(100)
def __parse_lockname(name):
    return int(hashlib.md5(name.encode()).hexdigest(), 16) % (2 ** 63)


def get_lock(pgconn, name, dotry=False):
    getlock = "pg_advisory_lock"
    name = __parse_lockname(name)
    if dotry:
        getlock = "pg_try_advisory_lock"
    with pgconn.cursor() as cursor:
        cursor.execute("SELECT {getlock}({name}) as l"
                       .format(getlock=getlock, name=name))
        if dotry:
            r = cursor.fetchone()
        else:
            return True

    return r[0]


def get_lock_transaction(pgconn, name, dotry=False):
    """Sets an transaction lock with the given name. Transaction lock is released upon commit or rollback.
    :param pgconn: Postgresql connection
    :param name: Name of lock
    param dotry: If True, tries to fetch lock and returns whether it was possible. If False, default,
        wait until lock is available.
    """
    getlock = "pg_advisory_xact_lock"
    name = __parse_lockname(name)
    if dotry:
        getlock = "pg_try_advisory_xact_lock"

    with pgconn.cursor() as cursor:
        cursor.execute("SELECT {getlock}({name}) as l"
                       .format(getlock=getlock, name=name))
        if dotry:
            r = cursor.fetchone()
        else:
            return True

    return r[0]


def release_lock(pgconn, name):
    name = __parse_lockname(name)
    unlock = "pg_advisory_unlock"
    with pgconn.cursor() as cursor:
        cursor.execute("SELECT {unlock}({name}) as l"
                       .format(unlock=unlock, name=name))
        r = cursor.fetchone()
    return r[0]


def get_table_partitions(pgconn, schema, table):
    get_partitions = """with recursive inh as (
       select i.inhrelid, null::text as parent
       from pg_catalog.pg_inherits i
         join pg_catalog.pg_class cl on i.inhparent = cl.oid
         join pg_catalog.pg_namespace nsp on cl.relnamespace = nsp.oid
       where nsp.nspname = '{s}' and cl.relname = '{t}'
       union all
       select i.inhrelid, (i.inhparent::regclass)::text
       from inh
         join pg_catalog.pg_inherits i on (inh.inhrelid = i.inhparent)
    )
    select c.relname as partition_name
    from inh
       join pg_catalog.pg_class c on inh.inhrelid = c.oid
       ORDER BY c.relname""".format(s=schema, t=table)
    output = []
    with pgconn.cursor() as cursor:
        cursor.execute(get_partitions)
        for p in cursor.fetchall():
            output.append(p[0])
    return output


def is_table_partitioned(pgconn, schema, table):
    get_partitions = """SELECT count(1) > 0 as exist 
FROM pg_partitioned_table 
WHERE partrelid::regclass::text=%s"""

    r = False
    with pgconn.cursor() as cursor:
        cursor.execute(get_partitions, (schema + "." + table,))
        r = cursor.fetchone()[0]
    return r
