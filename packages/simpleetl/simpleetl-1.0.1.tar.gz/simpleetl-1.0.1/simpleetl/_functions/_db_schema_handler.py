from simpleetl import LOG

from simpleetl._functions import _datatypes
from simpleetl._functions._db_quoting import quotelist, quote
from simpleetl._functions._dbfunctions import has_index, table_exists, column_type, has_fkey, \
    create_fkey, has_unique, \
    create_unique


def _ensure_lookupindex(pgcon, schema, table, cols, historic=False, unique=True):
    """

    :param dbcon:
    :param schema:
    :param table:
    :param hist:
    :return:
    """

    uniquesql = ""
    if unique:
        uniquesql = "UNIQUE"
    org_cols = None
    if historic:
        org_cols = cols.copy()
        cols.append("_validfrom")
        cols.append("_validto")
        cols.append("_version")

    if not has_index(pgcon, schema, table, cols):
        with pgcon.cursor() as cursor:
            cursor.execute("""CREATE {unique} INDEX ON {schema}.{table}
                        ({keycols});
                        """.format(schema=quote(schema, pgcon),
                                   table=quote(table, pgcon),
                                   unique=uniquesql,
                                   keycols=", ".join(quotelist(cols, pgcon))))
    # if historic:
    #    dbcon.dbexecute("""ALTER TABLE {schema}.{table} ADD UNIQUE ({keycols});"""
    #                    .format(schema=quote(schema, dbcon),
    #                            table=quote(table, dbcon),
    #                               keycols=", ".join(quotelist(org_cols, dbcon)))) 


def _ensure_structure(pgconn, factobj):
    factcols = factobj._get_cols_types(include_changeatts=True, include_ignorecols=True)
    partition_att = None
    if factobj.partitioning_enabled:
        partition_att = factobj.partition_attribute
    create_tab = _ensure_facttable_schema(pgconn, factobj.schema, factobj.table, factobj.key, factobj.keytype,
                                          factcols, partition_att=partition_att)
    lookupcols = factobj._get_cols(only_lookupatts=True)
    keycols = lookupcols.copy()
    if keycols is not None and keycols != [factobj.key]:
        # if keycols == [factobj.key] the primary key is the lookup attribute
        if not factobj.key_in_atts:
            keycols.append(factobj.key)

        _ensure_lookupindex(pgconn, factobj.schema, factobj.table, keycols)

        if lookupcols:
            if not has_unique(pgconn, factobj.schema, factobj.table, lookupcols):
                LOG.debug("Creating unique constraint on fact table")
                create_unique(pgconn, factobj.schema, factobj.table, lookupcols)

    if factobj.store_history:
        # factid = "_" + factobj.table + "_" + factobj.key
        partition_att_hist = None
        if factobj.partitioning_enabled_hist:
            partition_att_hist = factobj.partition_attribute_hist
        histkeycols = []
        if keycols:
            histkeycols += keycols.copy()
        # histkeycols.append(factid)
        addcols = [("_validfrom", _datatypes.timestamp_with_timezone),
                   ("_validto", _datatypes.timestamp_with_timezone),
                   ("_version", _datatypes.int)]

        histcols = factobj._get_cols_types(include_changeatts=False, include_ignorecols=True)
        create_hist = _ensure_facttable_schema(pgconn, factobj.schema, factobj.table_historic,
                                               factobj.key, factobj.keytype, histcols
                                               , addcols, partition_att=partition_att_hist)

        if keycols:
            _ensure_lookupindex(pgconn, factobj.schema, factobj.table_historic, keycols, True)
            lookupcols_validfrom = lookupcols.copy()
            lookupcols_validfrom.append("_validfrom")
            lookupcols_version = lookupcols.copy()
            lookupcols_version.append("_version")
            if not has_unique(pgconn, factobj.schema, factobj.table_historic, lookupcols_validfrom):
                LOG.debug("Creating unique constraint on historic table including _validfrom")
                create_unique(pgconn, factobj.schema, factobj.table_historic, lookupcols_validfrom)
            if not has_unique(pgconn, factobj.schema, factobj.table_historic, lookupcols_version):
                LOG.debug("Creating unique constraint on historic table including _version")
                create_unique(pgconn, factobj.schema, factobj.table_historic, lookupcols_version)

    _ensure_dimensions(pgconn, factobj.schema, factobj.table, factobj.dim_mappings)
    if factobj.store_history:
        _ensure_dimensions(pgconn, factobj.schema, factobj.table_historic, factobj.dim_mappings)
    pgconn.commit()


def _ensure_facttable_schema(pgconn, schema, table, key, keytype, columns, histcols=None,
                             partition_att=None):
    create_table = False
    partatt = ""
    partrange = ""
    prikey = quote(key, pgconn)
    if not table_exists(pgconn, schema, table):
        if partition_att is not None:
            partrange = "PARTITION BY RANGE ({c})".format(c=partition_att)
            if key != partition_att:
                # Postgresql requires partition key to be part of primart key
                prikey += ", " + quote(partition_att, pgconn)
            for col, datatype in columns:
                if col == partition_att:
                    partatt = "{n} {t},".format(n=quote(col, pgconn), t=datatype.sqltype())
                    break

        with pgconn.cursor() as cursor:
            cursor.execute("CREATE SCHEMA if not exists {sch};"
                           .format(sch=quote(schema, pgconn)))
            create_table = True
            tabcreate = """CREATE TABLE if not exists {sch}.{tab}
                ({k} {keytype} NOT NULL,
                {partatt}
            PRIMARY KEY ({prikey})
           ) {partrange}""".format(sch=quote(schema, pgconn),
                                   tab=quote(table, pgconn),
                                   k=quote(key, pgconn),
                                   prikey=prikey,
                                   keytype=keytype.sqltype(),
                                   partatt=partatt,
                                   partrange=partrange)
            cursor.execute(tabcreate)

    if histcols is not None:
        columns += histcols

    for col, datatype in columns:
        addcol(schema, table, pgconn, col, datatype)
    return create_table


def _ensure_dimensions(pgconn, schema, table, dim_mappings):
    for dim in dim_mappings:
        if not dim.fkey or not dim.insert:
            continue
        dstschema = dim.dimension._get_schema()
        dsttbl = dim.dimension._get_table()
        dstcol = dim.dimension._get_key()
        tablecol = dim.dstcol
        exists = has_fkey(pgconn, schema, table, tablecol, dstschema, dsttbl, dstcol)
        if not exists:
            try:
                create_fkey(pgconn, schema, table, tablecol, dstschema, dsttbl,
                            dstcol, True)
            except Exception as err:
                LOG.error("Problem creating foreign key {s1}.{t1}.{c1} -> {s2}.{t2}.{c2}"
                          .format(s1=schema, t1=table, c1=tablecol,
                                  s2=dstschema, t2=dsttbl, c2=dstcol))


def _create_temp_table(pgconn, factobj):
    # self.__lookupatts
    """Create temporary data storage, for loading data into."""

    with pgconn.cursor() as cursor:
        cursor.execute("CREATE SCHEMA IF NOT EXISTS tmp_data")

        cursor.execute(
            "DROP TABLE IF EXISTS tmp_data.{tmptable}".format(
                tmptable=quote(factobj.tmptable, pgconn)))
        factcols = factobj._get_cols_types(include_changeatts=True, include_ignorecols=True)
        create_tmp_tab = _ensure_facttable_schema(pgconn, "tmp_data", factobj.tmptable, factobj.key,
                                                  factobj.keytype, factcols)
        # When creating temporary table, we do not use a primary key, unless it is part of lookup attributes
        if not factobj.lookupatts or factobj.key not in factobj.lookupatts:
            cursor.execute(
                "ALTER TABLE tmp_data.{tmptable} DROP COLUMN {key};".format(key=quote(factobj.key, pgconn),
                                                                            tmptable=quote(factobj.tmptable,
                                                                                           pgconn)))


def _drop_temp_table(pgconn, factobj):
    """Create temporary data storage, for loading data into."""
    q = """DROP TABLE IF EXISTS tmp_data.{tmptable};
           """.format(schema=quote(factobj.schema, pgconn), tmptable=quote(factobj.tmptable, pgconn))
    with pgconn.cursor() as cursor:
        cursor.execute(q)


def _ensure_indexes(pgconn, factobj):
    idx = """CREATE INDEX ON {schema}.{table}
                            ({keycols});"""

    for idxcols in factobj.indexes:
        if not has_index(pgconn, factobj.schema, factobj.table, idxcols):
            LOG.debug("Creating index on columns: " + ",".join(idxcols))
            with pgconn.cursor() as cursor:
                cursor.execute(idx.format(schema=quote(factobj.schema, pgconn),
                                          table=quote(factobj.table, pgconn),
                                          keycols=", ".join(quotelist(idxcols, pgconn))))
        # if (factobj.store_history and
        #        not dbcon.has_index(factobj.schema, factobj.table_historic, idxcols)):
        #    dbcon.dbexecute(idx.format(schema=quote(factobj.schema, dbcon),
        #                               table=quote(factobj.table_historic, dbcon),
        #                               keycols=", ".join(quotelist(idxcols, dbcon))))


def addcol(schema, table, pgconn, col, datatype):
    coltype = column_type(pgconn, schema, table, col)
    if coltype is not None:
        if coltype.replace(" NOT NULL", "").upper() != datatype.sqltype().replace(" NOT NULL", "").upper():
            LOG.warning("Wrong datatype ({tnow}). Consider running ALTER TABLE {s}.{t} ALTER COLUMN {c} TYPE {ty};"
                        .format(s=schema, t=table, c=col,
                                ty=datatype.sqltype().replace(" NOT NULL", ""),
                                tnow=coltype.replace(" NOT NULL", "")))
        # Test if current datatype allows NULL and whether NULLs should be allowed
        if ("NOT NULL" not in coltype.upper()) != datatype.allow_null:
            setval = "SET NOT NULL"
            if datatype.allow_null:
                setval = "DROP NOT NULL"
            q = "ALTER TABLE {s}.{t} ALTER COLUMN {c} {set}".format(s=schema, t=table, c=col, set=setval)
            LOG.warning("Wrong NULL settings. Consider running " + q)
    else:
        null = ""

        if not datatype.allow_null:
            null = " NOT NULL"
        with pgconn.cursor() as cursor:
            cursor.execute('ALTER TABLE {sc}.{tab} ADD COLUMN {n} {t} {null}'
                           .format(sc=quote(schema, pgconn),
                                   tab=quote(table, pgconn),
                                   n=quote(col, pgconn),
                                   t=datatype.sqltype(),
                                   null=null))
