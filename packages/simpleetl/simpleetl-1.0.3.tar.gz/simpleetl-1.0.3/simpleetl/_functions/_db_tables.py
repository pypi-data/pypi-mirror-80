from pygrametl.tables import BulkFactTable, _quote
import pygrametl


def _get_bulktable(pygramcon, schema, table, keyrefs, measures, incl_id=None):
    # keyrefs = self.get_cols(atts=False)
    # measures = self.get_cols(dims=False)

    if incl_id is not None:
        measures.append(incl_id)

    facttable = BulkFactTable(name=_quote(schema) + "." + _quote(table),
                              keyrefs=keyrefs,
                              measures=measures,
                              bulkloader=generate_bulkloader(pygramcon),
                              fieldsep='\t',
                              rowsep='\n',
                              nullsubst="\\N",
                              tempdest=None,
                              bulksize=100000,
                              usefilename=False,
                              dependson=(),
                              strconverter=getdbfriendlystr)

    return facttable


def _get_bulkhisttable(pygramcon, schema, table, table_historic, keyrefs, measures, key, incl_id=None):
    measures += ['_validfrom', '_validto', '_version']
    if incl_id is not None:
        measures.append(incl_id)

    facttable = BulkFactTable(name=_quote(schema) + "." + _quote(table_historic),
                              keyrefs=keyrefs,
                              measures=measures,
                              bulkloader=generate_bulkloader(pygramcon),
                              fieldsep='\t',
                              rowsep='\n',
                              nullsubst="\\N",
                              tempdest=None,
                              bulksize=100000,
                              usefilename=False,
                              dependson=(),
                              strconverter=getdbfriendlystr)
    return facttable


def generate_bulkloader(pygramcon):
    def pgcopybulkloader(name, atts, fieldsep, rowsep, nullval,
                         filehandle):
        """ A bulk loader method for loading data into the data warehouse.

        This is an interface between pygrametl and psycopg2, hence the argument
        list is required for pygrametl to be working.

        :param name: Table name.
        :param atts: Column names to insert into.
        :param fieldsep: Seperator of the CSV file.
        :param rowset: Row seperator of the CSV file. Not used by psycopg2, but
            required for pygrametl to be working.
        :param nullval: Null value.
        :param filehandler: A file handler, from where the data is loaded from.
        """

        with pygramcon.cursor() as cursor:
            cursor.copy_from(file=filehandle, table=name, sep=fieldsep,
                             null=str(nullval),
                             columns=[pygrametl.tables._quote(xn) for xn in atts])

    return pgcopybulkloader


def getdbfriendlystr(value, nullvalue='None'):
    """Covert a value into a string that can be accepted by a DBMS.

       None values are converted into the value of the argument nullvalues
       (default: 'None'). Bools are converted into '1' or '0' (instead of
       'True' or 'False' as str would do). Other values are currently just
       converted by means of str.

    """
    if value is None:
        return nullvalue
    elif isinstance(value, bool):
        if value:
            return "1"
        else:
            return "0"
    elif isinstance(value, str):
        return value.replace("\n", "\\n").replace("\t","\\t").replace("\r","\\r")
    else:
        return str(value)
