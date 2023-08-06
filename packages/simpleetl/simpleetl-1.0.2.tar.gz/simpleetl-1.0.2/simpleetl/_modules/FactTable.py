import sys
from simpleetl import Dimension
from simpleetl import LOG
from simpleetl._functions import _datatypes as dt
from simpleetl._modules.Dimension import Column, DimColumn
from simpleetl import datatypes
from functools import lru_cache


class FactTable:
    def __init__(self, schema, table,
                 lookupatts=None,
                 store_history=False,
                 migrate_updates=True,
                 key=None,
                 ignore_atts=None,
                 track_last_updated=False,
                 track_created=False,
                 tmptable=None):
        """
        :param schema: Database schema for fact table
        :param table: Database table for fact table
        :param lookupatts: A list of attributes which uniquely defines a row. Will enable handling of changes to facts.
        :param store_history: Will store a complete track of changes to facts in a seperate table.
        :param migrate_updates: Update facts when changes are deteted in source data.
        :param key: Primary key name.
        :param ignore_atts: List of attributes, where changes will be ignore.
        :param track_last_updated: Add an attribute for tracking last changed timestamp of a fact.
        :param track_created: Add an attribute for tracking when a fact is created.
        :param tmptable: Temporary table, stored in the tmp_data schema. Lock on this table will ensure only single ETL
        on this table at a time. If none, generated from schema and table name.
        """
        self.__schema = schema
        self.__table = table
        self.__store_history = store_history
        self.__lookupatts = None
        self.__ignore_atts = []
        self.__track_last_updated = track_last_updated
        self.__track_created = track_created
        self.__migrate_updates = migrate_updates
        if ignore_atts:
            self.__ignore_atts = ignore_atts.copy()
        if lookupatts:
            assert isinstance(lookupatts, list), "Lookup attributs must be a list"
            self.__lookupatts = lookupatts.copy()  # Make a copy of the list using .copy(), as the list is parsed by
        elif store_history:
            LOG.error("History cannot be preserved when no lookupatts have been defined")
            sys.exit(1)

        # reference. If we didn't do this, the caller could later change the lookupatts.

        self.__table_historic = None
        self.__deleted_rows_method = False
        self.__handle_deleted_rows_func = None
        self.__deleted_mark_keep_days = None
        self.__deleted_rows_limit = None

        self.__key = key == None and "id" or key  # set key to 'id' if key is None
        self.__keytype = datatypes.bigint_notnull
        self.__key_in_atts = False
        self.__ignore_pk_in_atts_warning = False

        if self.__store_history:
            self.__table_historic = self.__table + "_historic"

        self.__simple_mappings = []
        self.__dim_mappings = []

        self.__indexes = []

        self.__prepared = False

        self.__col_order = []
        if tmptable:
            self.__tmptable = "_".join([self.__schema, tmptable, "tmp"])
        else:
            self.__tmptable = "_".join([self.__schema, self.__table, "tmp"])

        self.__partition_attribute = None
        self.__partitionfunc = None
        self.__partitions_used = set()

        self.__partition_attribute_hist = None
        self.__partitionfunc_hist = None
        self.__partitions_used_hist = set()

    @property
    def schema(self):
        return self.__schema

    @property
    def table(self):
        return self.__table

    @property
    def tmptable(self):
        return self.__tmptable

    @property
    def table_historic(self):
        return self.__table_historic

    @property
    def store_history(self):
        return self.__store_history

    @property
    def track_last_updated(self):
        return self.__track_last_updated

    @property
    def track_created(self):
        return self.__track_created

    @property
    def migrate_updates(self):
        return self.__migrate_updates

    @property
    def lookupatts(self):
        return self.__lookupatts and self.__lookupatts.copy() or None

    # def add_lookupatt(self, att):
    #    self.__lookupatts.append(att)

    @property
    def deleted_rows_method(self):
        return self.__deleted_rows_method

    @property
    def handle_deleted_rows_func(self):
        return self.__handle_deleted_rows_func

    @property
    def deleted_mark_keep_days(self):
        return self.__deleted_mark_keep_days

    @property
    def deleted_rows_limit(self):
        return self.__deleted_rows_limit

    @property
    def key(self):
        return self.__key

    @property
    def keytype(self):
        return self.__keytype

    @property
    def simple_mappings(self):
        return self.__simple_mappings

    @property
    def dim_mappings(self):
        return self.__dim_mappings

    @property
    def indexes(self):
        return self.__indexes

    @property
    def key_in_atts(self):
        return self.__key_in_atts

    @property
    def ignore_pk_in_atts_warning(self):
        return self.__ignore_pk_in_atts_warning

    """ Properties and methods related to table partitioning """

    @property
    def partitioning_enabled(self):
        return self.__partition_attribute is not None

    @property
    def partitioning_enabled_hist(self):
        return self.__partition_attribute_hist is not None

    @property
    def partition_attribute(self):
        return self.__partition_attribute

    @property
    def partition_attribute_hist(self):
        return self.__partition_attribute_hist

    def get_partition(self, row):
        return self.__get_partition_att(row[self.__partition_attribute])

    def get_partition_hist(self, row):
        return self.__get_partition_att_hist(row[self.__partition_attribute_hist])

    @lru_cache(1000)
    def __get_partition_att(self, value):
        return self.__partitionfunc(value)

    @lru_cache(1000)
    def __get_partition_att_hist(self, value):
        return self.__partitionfunc_hist(value)

    def add_used_partition(self, partition):
        self.__partitions_used.add(partition)

    def add_used_partition_hist(self, partition):
        self.__partitions_used_hist.add(partition)

    @property
    def used_partitions(self):
        plist = list(self.__partitions_used)
        plist.sort(key=lambda x: x[0])
        return plist

    @property
    def used_partitions_hist(self):
        plist = list(self.__partitions_used_hist)
        plist.sort(key=lambda x: x[0])
        return plist

    def enable_partitioning(self, attribute, partitionfunc):
        """Enables range parition on fact table.
        :param attribute: Attribute, which must be part of lookup attributes, to partition by.
        :param partitionfunc: Function, which takes an input value and returns a tuple of 3 values:
            (table_suffix, range_start, range_end). Example: A table partitioned on a date column with partitions per year
            could return on input 2020-03-10: ('2020', '2020-01-01', '2021-01-01').
            * PLEASE NOTE, the range_end is exclusive.
            * The function will be executed wrapped in a cache, to prevent expensive calculations to be repeated.
        """

        assert attribute in self.__lookupatts, (
                "Partition attribute " + str(attribute) + " must be part of lookup attributes on table, as PostgreSQL"
                                                          " requires partition key to be part of unique indexes.")
        self.__partition_attribute = attribute
        self.__partitionfunc = partitionfunc

    def enable_partitioning_historic(self, attribute, partitionfunc):
        """Enables range parition on historic fact table.
        :param attribute: Attribute, which must be part of lookup attributes, to partition by.
        :param partitionfunc: Function, which takes an input value and returns a tuple of 3 values:
            (table_suffix, range_start, range_end). Example: A table partitioned on a date column with partitions per year
            could return on input 2020-03-10: ('2020', '2020-01-01', '2021-01-01').
            * PLEASE NOTE, the range_end is exclusive.
            * The function will be executed wrapped in a cache, to prevent expensive calculations to be repeated.
        """

        assert attribute in self.__lookupatts, (
                "Partition attribute " + str(
            attribute) + " on historic table must be part of lookup attributes on table, as PostgreSQL"
                         " requires partition key to be part of unique indexes.")
        self.__partition_attribute_hist = attribute
        self.__partitionfunc_hist = partitionfunc

    def set_ignore_pk_in_atts_warning(self):
        """Silense warnings when adding attribute matching primary key"""
        self.__ignore_pk_in_atts_warning = True

    def add_dim_mapping(self, dimension, dstcol, namemapping={}, inject=False, insert_to_facttable=True,
                        fkey=True, index=True, allow_null=False):
        """Adds a dimension to the fact table.

        :param dimension: Dimension object
        :param dstcol: Destination column of fact table
        :param namemapping: Optional dictinary mapping for dimension. E.g., if dimension expects "datekey" but we have
        "invoicedate" from source, namemapping would be {"datekey":"invoicedate"}
        :param inject: Inject found key/val into src data, e.g., for use with other dimension lookups.
        :param insert_to_facttable: Insert dimension key into fact table if True.
        :param fkey: Create foreing key to dimension.
        :param index: Create index on column.
        :param allow_null: Allow null values to column
        """
        if not isinstance(dimension, Dimension):
            LOG.error(
                "add_dim_mapping " + dstcol + " dimension must be a Dimension() object. Got " + str(type(dimension)))
            sys.exit(1)

        if not isinstance(dstcol, str) or not dstcol:
            LOG.error("add_column_mapping dstcol must be a string. Input value: " + str(dstcol))
            sys.exit(1)

        if not isinstance(namemapping, dict):
            LOG.error("add_column_mapping " + dstcol + " namemapping must be a dictionary. Input type: " + str(
                type(namemapping)))
            sys.exit(1)

        for tp, k in self.__col_order:
            if k.dstcol == dstcol:
                LOG.error("add_column_mapping column allready added before. Column: " + str(dstcol))
                sys.exit(1)

        if not inject and not insert_to_facttable:
            LOG.error("Neither injecting dimension" + dimension._get_full_table() + "/" + dstcol +
                      " into source data or insertering into table, does not make use of dimension at all.")
            sys.exit(1)

        if not isinstance(fkey, bool):
            LOG.error("fkey must be boolean. Found " + str(fkey) + " of type " + str(type=fkey))
            sys.exit(1)
        if not isinstance(fkey, bool):
            LOG.error("index must be boolean. Found " + str(index) + " of type " + str(type=index))
            sys.exit(1)
        if dstcol == self.__key and not self.__ignore_pk_in_atts_warning:
            LOG.warning(dstcol + " is the same as primary key")
            self.__key_in_atts = True
            self.__keytype = dimension._get_keytype()
        if dstcol == self.__partition_attribute and allow_null:
            LOG.error("column " + dstcol + " is partition key and therefore must not be null.")
            sys.exit(1)
        if dstcol == self.__partition_attribute_hist and allow_null:
            LOG.error("column " + dstcol + " is partition key on historic table and therefore must not be null.")
            sys.exit(1)

        d = DimColumn(dimension, dstcol, namemapping, inject, insert_to_facttable, fkey, allow_null)

        self.__dim_mappings.append(d)
        self.__col_order.append(("d", d))
        if insert_to_facttable and index:
            self.add_index([dstcol])
        return

    def add_column_mapping(self, srccol, datatype, dstcol=None):
        """ Maps a value from source data to destination table.
        :param srccol: Source data column to use.
        :param datatype: Datatype of source data.
        :param dstcol: Name of destination column.
        """
        if not isinstance(srccol, str) or not srccol:
            LOG.error("add_column_mapping srccol must be a string. Input value: " + str(srccol))
            sys.exit(1)
        if dstcol is not None and not isinstance(dstcol, str):
            LOG.error("add_column_mapping dstcol must be a string. Input value: " + str(dstcol))
            sys.exit(1)

        if dstcol is None:
            dstcol = srccol

        for tp, k in self.__col_order:
            if k.dstcol == dstcol:
                LOG.error("add_column_mapping column allready added before. Column: " + str(dstcol))
                sys.exit(1)

        if dstcol == self.__partition_attribute and datatype.allow_null:
            LOG.error("column " + dstcol + " is partition key and therefore must not be null.")
            sys.exit(1)

        if dstcol == self.__partition_attribute_hist and datatype.allow_null:
            LOG.error("column " + dstcol + " is partition key on historic table and therefore must not be null.")
            sys.exit(1)

        if dstcol == self.__key and not self.__ignore_pk_in_atts_warning:
            LOG.warning(dstcol + " is the same as primary key")
            self.__key_in_atts = True
            datatype = datatype.copy(False)  # Ensure we disallow NULL
            self.__keytype = datatype

        if self.__lookupatts and dstcol in self.__lookupatts:
            datatype.copy(False)  # Ensure we disallow NULL
        c = Column(srccol, dstcol, datatype)
        self.__simple_mappings.append(c)
        self.__col_order.append(("c", c))

    def handle_deleted_rows(self, method="date", limitfunc=None, keep_days=None,
                            limit_deleted_rows=None):
        """Propagates deleted rows from source file to database.
        :param method: Determine how to handle deletes:
            "date": Mark deleted row in versioned table with an time stamp to _validto column. Deletes from T1 fact table.
            "mark": Add additional _deleted measure to fact table and versioned table. Will also mark _validto with end of life time stamp.
            "wipe": Completely wipes removed data from both T1 fact table and versioned fact table.
        :param limitfunc: a function returning a a SQL WHERE limit clause to constrain which rows will be deleted.
        :param keep_days: If set to an integer, delete marked data after keep_days days + 6 hours.
        :param limit_deleted_rows: Raise an error if more than n rows are deleted in a batch. Applies for non-historic table.
        """
        if self.lookupatts is None:
            LOG.error("Deleted rows cannot be handled when no lookupatts are defined.")
            sys.exit(1)
        if method not in ("date", "mark", "wipe"):
            LOG.error("Invalid value for handle_deleted_rows method: " + str(method))
            sys.exit(1)
        self.__deleted_rows_method = method
        self.__handle_deleted_rows_func = limitfunc
        if isinstance(keep_days, int):

            assert method == "mark", (
                    "When keep_days is set, method must be mark. Defined method is " + str(method))
            self.__deleted_mark_keep_days = int(keep_days)

        if limit_deleted_rows is not None:
            assert isinstance(limit_deleted_rows, int), (
                    "limit_deleted_rows must be an integer. Found " + str(type(limit_deleted_rows)))
            assert limit_deleted_rows > 0, (
                    "limit_deleted_rows must be greater than 0. Got " + str(limit_deleted_rows))
            self.__deleted_rows_limit = limit_deleted_rows

    def add_index(self, columns):
        """ Adds an index over a list of columns. This index is will be checked for existance at every ETL run.

        :param columns: List of columns to index in one index.
        """
        if not isinstance(columns, list):
            LOG.error("Index list must be list!")
            sys.exit(1)
        self.__indexes.append(columns)

    def _get_cols_types(self, dims=True, atts=True, include_lookupatts=True, only_lookupatts=False,
                        use_srccol=False, include_ignorecols=False, include_changeatts=False):
        """

        :param dims:
        :param atts:
        :param include_lookupatts:
        :param only_lookupatts:
        :param use_srccol:
        :param include_ignorecols:
        :param include_changeatts:
        :return:
        """
        cols = []
        for c_type, c_elem in self.__col_order:
            if dims and c_type == "d":  # Handle dimension mapping

                if not c_elem.insert:
                    continue  # Do not insert into table, dimension value only for looking up data
                if not include_ignorecols and c_elem.dstcol in self.__ignore_atts:
                    continue  # Ignore changes to this dimension attribute
                if use_srccol and len(c_elem.namemapping) > 0:

                    for nkey, n in c_elem.namemapping.items():
                        # nsrc = c.namemapping.get(nkey, n)

                        cdatatype = c_elem.dimension.get_lookuptype(nkey).copy(allow_null=c_elem.allow_null)

                        cols.append((n, cdatatype))
                elif use_srccol:
                    for srccol, srctype, defval in c_elem.dimension.get_lookupatts():
                        cols.append((srccol, srctype))
                else:

                    cdatatype = c_elem.dimension._get_keytype().copy(allow_null=c_elem.allow_null)
                    cols.append((c_elem.dstcol, cdatatype))
            elif atts and c_type == "c":  # Handle attribute mapping
                if not include_ignorecols and c_elem.dstcol in self.__ignore_atts:
                    continue  # Ignore changes to this attribute
                if include_ignorecols and not include_changeatts and c_elem.dstcol in ("_updated", "_deleted"):
                    continue  # Ignore last updated attribute
                if use_srccol:
                    cols.append((c_elem.srccol, c_elem.datatype))
                else:
                    cols.append((c_elem.dstcol, c_elem.datatype))

        # Remove lookup attributes, if we do not want these.
        if not include_lookupatts and self.lookupatts:
            cols2 = []
            for c in cols:
                if c[0] not in self.lookupatts:
                    cols2.append(c)
            cols = cols2

        if only_lookupatts:
            if self.lookupatts:
                c2 = []
                for c in cols:
                    if c[0] in self.lookupatts:
                        c2.append(c[0])
                if len(c2) != len(self.lookupatts):
                    errstr = "Lookup attribute missing: Defined colums: (" + str(c2) + "). Expected columns: " + str(
                        self.lookupatts)
                    LOG.error(errstr)
                    raise AttributeError(errstr)
                cols = [(c,) for c in self.lookupatts]
            else:
                cols = []

        return cols

    def _get_cols(self, dims=True, atts=True, include_lookupatts=True, only_lookupatts=False, use_srccol=False,
                  include_ignorecols=False, include_changeatts=False):
        """

        :param dims:
        :param atts:
        :param include_lookupatts:
        :param only_lookupatts:
        :param use_srccol:
        :param include_ignorecols:
        :param include_changeatts:
        :return:
        """
        cols = self._get_cols_types(dims, atts, include_lookupatts, only_lookupatts, use_srccol, include_ignorecols,
                                    include_changeatts)
        cols = [c[0] for c in cols]
        return cols

    def _get_srccols(self):
        cols = []
        injectcols = []
        for c in self.__dim_mappings:
            if not c.insert:
                continue
            for srccol, srctype, defval in c.dimension.get_lookupatts():

                cols.append(c.namemapping.get(srccol, srccol))
                if c.inject:
                    injectcols.append(c.dstcol)
        cols += [c.srccol for c in self.__simple_mappings]
        cols = set(cols)
        for c in injectcols:
            cols.remove(c)

        return list(cols)

    def _validate_structure(self):
        latts = self._get_cols(only_lookupatts=True)
        if latts and self.lookupatts:
            for latt in self.lookupatts:
                if latt not in latts:
                    LOG.error('Lookup attribute "' + latt + '" is not defined as an attribute on the fact table')
                    sys.exit(1)

    def _prepare_run(self):
        if self.__prepared:
            LOG.error("Fact table prepare_run has allready been executed once!")
            sys.exit(1)
        self.__prepared = True
        if self.__track_last_updated:
            LOG.debug("Tracking updates")
            self.add_column_mapping("_updated", dt.timestamp)
            self.add_index(["_updated"])
            self.__ignore_atts.append("_updated")

        if self.__track_created:
            LOG.debug("Tracking created timestamp")
            self.add_column_mapping("_created", dt.timestamp)
            self.add_index(["_created"])
            self.__ignore_atts.append("_created")

        if self.deleted_rows_method == "mark":
            self.add_column_mapping("_deleted", dt.timestamp)
            self.add_index(["_deleted"])
            self.__ignore_atts.append("_deleted")

