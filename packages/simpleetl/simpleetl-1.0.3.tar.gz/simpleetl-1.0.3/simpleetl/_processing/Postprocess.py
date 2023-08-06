import time
import traceback
from multiprocessing import Value, Lock
from multiprocessing.pool import ThreadPool

import psycopg2
from psycopg2.extras import RealDictCursor
from pygrametl import ConnectionWrapper

from simpleetl import CONFIG
from simpleetl import LOG
from simpleetl._functions import _db_schema_handler as schand
from simpleetl._functions._db_get_nextid import _get_nextid
from simpleetl._functions._db_quoting import quote, quotelist
from simpleetl._functions._db_tables import _get_bulkhisttable
from simpleetl._functions._db_tables_scd import SlowlyChangingDimension
from simpleetl._functions._dbfunctions import table_exists, get_table_partitions, is_table_partitioned


class ETLPostprocess():
    def __init__(self, facttable, batchlog, data_timestamp, db_dsn):
        self.__facttable = facttable
        self.__batchlog = batchlog
        self.__data_timestamp = data_timestamp
        self.__db_dsn = db_dsn

        self.__lock = Lock()
        self.__updated_reg = Value("i", 0)
        self.__updated_hist = Value("i", 0)
        self.__inserted_reg = Value("i", 0)
        self.__inserted_hist = Value("i", 0)
        self.__deleted_reg = Value("i", 0)
        self.__deleted_hist = Value("i", 0)

    def final_load(self):
        """ ---------- Post processing preparing tables ---------- """

        pgconn = psycopg2.connect(self.__db_dsn)

        self.__batchlog.set_prepare_load_start()

        LOG.info("Preparing tables for loading data")

        try:
            lookupatts = self.__facttable._get_cols(only_lookupatts=True)
            if lookupatts:
                schand._ensure_lookupindex(pgconn, "tmp_data", self.__facttable.tmptable,
                                           lookupatts, unique=True)
        except psycopg2.IntegrityError as err:
            LOG.error("Duplicate facts detected. We cannot proceed! (" + str(err) + ")")
            pgconn.close()
            return False
        pgconn.commit()
        is_partitioned = False
        if self.__facttable.partitioning_enabled:
            is_partitioned = is_table_partitioned(pgconn, self.__facttable.schema, self.__facttable.table)
            if is_partitioned:
                self.__prepare_partitions(pgconn, self.__facttable.table, self.__facttable.used_partitions)
            else:
                LOG.warning("Table is designed to be partitioned, but table in database is not partitioned")
        is_partitioned_hist = False
        if self.__facttable.partitioning_enabled_hist:
            is_partitioned_hist = is_table_partitioned(pgconn, self.__facttable.schema, self.__facttable.table_historic)
            if is_partitioned_hist:
                self.__prepare_partitions(pgconn, self.__facttable.table_historic,
                                          self.__facttable.used_partitions_hist)
            else:
                LOG.warning("Historic table is designed to be partitioned, but table in database is not partitioned")
        try:
            """ ---------- Migrate updates ---------- """
            tp = ThreadPool(2)
            if self.__facttable.lookupatts is not None and self.__facttable.migrate_updates:
                LOG.info("Migrating updates..")
                pupd = tp.apply_async(self._migrate_update_changed_data_reg)
                if self.__facttable.store_history:
                    p2upd = p = tp.apply_async(self._migrate_update_changed_data_hist)
                    p2upd.get()
                pupd.get()

                self.__batchlog.set_migrate_update_done(self.__updated_reg.value, self.__updated_hist.value)

            """ ---------- Insert new data ---------- """
            LOG.info("Migrating new data..")

            pins = tp.apply_async(self._migrate_insert_new_data_reg)

            if self.__facttable.store_history and self.__facttable.lookupatts:
                p2ins = tp.apply_async(self._migrate_insert_new_data_hist)
                p2ins.get()

            pins.get()

            self.__batchlog.set_migrate_insert_done(self.__inserted_reg.value, self.__inserted_hist.value)

            """ ---------- Remove deleted data ---------- """

            if self.__facttable.deleted_rows_method and self.__facttable.lookupatts:
                LOG.info("Marking removed rows..")
                pdel = tp.apply_async(self._propagate_deleted_data_reg)

                if self.__facttable.store_history:
                    p2del = tp.apply_async(self._propagate_deleted_data_hist)
                    p2del.get()

                pdel.get()
                self.__batchlog.set_migrate_removed_done(self.__deleted_reg.value, self.__deleted_hist.value)
            tp.close()
            if self.is_shutdown():
                return False

            """ ---------- Finalize ---------- """
            # Clean up temporary table
            if CONFIG.debug:
                LOG.warning(
                    "Temporary tables are NOT dropped, due to DEBUG. These will be overwritten on next execution of this job")
            else:
                schand._drop_temp_table(pgconn, self.__facttable)
            pgconn.commit()

            """ ---------- Done ---------- """
            self.__batchlog.set_batch_done()
        except Exception as err:
            tb = traceback.print_exc()
            LOG.error(err, tb)
            return False
        if self.__facttable.partitioning_enabled and is_partitioned:
            self.__remove_unused_partitions(pgconn, self.__facttable.table)
        if self.__facttable.partitioning_enabled_hist and is_partitioned_hist:
            self.__remove_unused_partitions(pgconn, self.__facttable.table_historic)
        pgconn.close()
        return True

    def __prepare_partitions(self, pgconn, table, partitions):
        """Create missing partitions
        """
        schema = self.__facttable.schema
        for suffix, range_from, range_to in partitions:
            partition = table + "_" + suffix
            if not table_exists(pgconn, schema, partition):
                with pgconn.cursor() as cursor:
                    q = """CREATE TABLE {s}.{p} PARTITION OF {s}.{t}
                    FOR VALUES FROM ({fr}) TO ({to})""".format(s=schema, t=table, p=partition,
                                                               fr=range_from, to=range_to)
                    LOG.debug("Creating new partition {s}.{p}".format(s=schema, p=partition))
                    cursor.execute(q)
        pgconn.commit()

    def __remove_unused_partitions(self, pgconn, table):
        """ Remove unused partitions
        """
        # Source: https://www.postgresql.org/message-id/otalb9%245ma%241%40blaine.gmane.org
        schema = self.__facttable.schema

        partition_exists = "select exists(select * from {s}.{p})"
        partitions = get_table_partitions(pgconn, schema, table)
        with pgconn.cursor() as cursor:
            for partition in partitions:

                cursor.execute(partition_exists.format(s=schema, p=partition))
                has_data = cursor.fetchone()[0]
                if not has_data:
                    LOG.debug("Remove empty partition {s}.{p}".format(s=schema, p=partition))
                    cursor.execute("DROP TABLE {s}.{p}".format(s=schema, p=partition))
        pgconn.commit()

    def _migrate_update_changed_data_reg(self):
        t0 = time.time()
        atts = self.__facttable._get_cols()
        keycols = self.__facttable._get_cols(only_lookupatts=True)

        measurecols = self.__facttable._get_cols(include_lookupatts=False, include_ignorecols=False)
        updatecols = self.__facttable._get_cols(include_lookupatts=False, include_ignorecols=True,
                                                include_changeatts=True)
        if len(set(atts).difference(keycols)) == 0:
            return

        pgconn = psycopg2.connect(self.__db_dsn,
                                  application_name="SimpleETL Updater {s}.{t}".format(s=self.__facttable.schema,
                                                                                      t=self.__facttable.table))
        pygramcon = ConnectionWrapper(pgconn)
        histwhere = []

        histcheck = ["c.{col} = b.{col}".format(col=quote(c, pgconn)) for c in keycols]

        updcols = []
        # measurecols = self.get_cols(include_lookupatts=False)
        for c in measurecols:
            histwhere.append("b.{col} IS DISTINCT FROM c.{col}".format(col=quote(c, pgconn)))

        for c in updatecols:
            updcols.append("{col} = x.{col}".format(col=quote(c, pgconn)))

        ign_deleted = ""
        if self.__facttable.deleted_rows_method == "mark":
            histwhere.append("b._deleted IS DISTINCT FROM c._deleted")
        orgid = ""
        if not self.__facttable.key_in_atts:
            orgid = "b.{key}, ".format(key=quote(self.__facttable.key, pgconn))
        tmptable = """CREATE TEMPORARY TABLE tmptable AS
            SELECT {orgid} c.* from tmp_data.{tmptable} c
            JOIN {schema}.{table} b
                ON ({existcheck}) 
                    AND ({changecheck})
        """.format(schema=quote(self.__facttable.schema, pgconn),
                   table=quote(self.__facttable.table, pgconn),
                   orgid=orgid,
                   tmptable=quote(self.__facttable.tmptable, pgconn),
                   existcheck=" AND ".join(histcheck),
                   changecheck=" OR ".join(histwhere))

        changeddata = """UPDATE {schema}.{table} a SET {upd}
        FROM tmptable x WHERE a.{key} = x.{key}
            """.format(schema=quote(self.__facttable.schema, pgconn),
                       table=quote(self.__facttable.table, pgconn),
                       upd=", ".join(updcols),
                       key=quote(self.__facttable.key, pgconn))
        if CONFIG.debug:
            LOG.debug("SQL for updating data from regular table:\n" + tmptable +
                      "\n\n" + changeddata)
        with pgconn.cursor() as cursor:
            cursor.execute(tmptable)
            cursor.execute(changeddata)
            upddata = cursor.rowcount

        if CONFIG.simulate:
            pygramcon.rollback()
        else:
            pygramcon.commit()
        pygramcon.close()
        tsstr = time.strftime("%H:%M:%S", time.gmtime(time.time() - t0))
        LOG.info("Updated fact table. {u} rows updated in {t}.".format(u=upddata, t=tsstr))
        with self.__lock:
            self.__updated_reg.value = upddata

    def _migrate_update_changed_data_hist(self):
        t0 = time.time()
        keycols = self.__facttable._get_cols(only_lookupatts=True)
        atts = self.__facttable._get_cols()

        measurecols = self.__facttable._get_cols(include_lookupatts=False, include_ignorecols=False)
        updatecols = self.__facttable._get_cols(include_lookupatts=False, include_ignorecols=True,
                                                include_changeatts=False)

        if len(set(atts).difference(keycols)) == 0:
            return

        pgconn = psycopg2.connect(self.__db_dsn,
                                  application_name="SimpleETL Updater {s}.{t}".format(s=self.__facttable.schema,
                                                                                      t=self.__facttable.table))
        pygramcon = ConnectionWrapper(pgconn)
        histwhere = []

        histcheck = []
        histcheck2 = []
        vercheck = []
        for c in keycols:
            histcheck.append("a.{col} = b.{col}".format(col=quote(c, pgconn)))
            histcheck2.append("a.{col} = c.{col}".format(col=quote(c, pgconn)))
            vercheck.append("a.{col} = x.{col}".format(col=quote(c, pgconn)))

        updcols = []

        # id = _get_nextid(dbcon, factobj.schema, factobj.table_historic, factobj.key)
        for c in measurecols:
            histwhere.append("a.{col} IS DISTINCT FROM b.{col}".format(col=quote(c, pgconn)))
        for c in updatecols:
            updcols.append("{col} = {{{col2}}}".format(col=quote(c, pgconn), col2=c))

        changeddata = """SELECT  a.*
    FROM tmp_data.{tmptable} a
    JOIN {schema}.{histtable} b
        ON {existcheck} 
            AND ((_validto is NULL
                    AND ({changecheck}))
                    -- Valid data row exists, update from this
                OR NOT EXISTS (SELECT 1 FROM {schema}.{histtable} c WHERE _validto IS NULL AND {existcheck2})
                        -- Data row was earlier deleted, but Slowly Changing Dimension handles recreation of this.
                    )

            """.format(schema=quote(self.__facttable.schema, pgconn),
                       table=quote(self.__facttable.table, pgconn),
                       tmptable=quote(self.__facttable.tmptable, pgconn),
                       key=quote(self.__facttable.key, pgconn),
                       vercheck=" AND ".join(vercheck),
                       histtable=quote(self.__facttable.table_historic, pgconn),
                       existcheck=" AND ".join(histcheck),
                       existcheck2=" AND ".join(histcheck2),
                       changecheck=" OR ".join(histwhere))
        if CONFIG.debug:
            LOG.debug("SQL for updating data from historic table:\n" + changeddata)
        if self.__data_timestamp is not None:
            def cd(x, y, z):
                return self.__data_timestamp

            custd = cd
        else:
            custd = None
        t2atts = atts + ['_validfrom', '_validto', '_version']
        histtable = SlowlyChangingDimension(
            self.__facttable.schema + "." + self.__facttable.table_historic,
            key=self.__facttable.key,
            attributes=t2atts,
            lookupatts=keycols,
            fromatt="_validfrom",
            toatt="_validto",
            fromfinder=custd,
            tofinder=custd,
            versionatt="_version",
            cachesize=0,
            prefill=False,
            usefetchfirst=True,
            targetconnection=pygramcon
        )
        upddata = 0
        with pgconn.cursor("Changed historic data", cursor_factory=RealDictCursor) as cursor:
            cursor.execute(changeddata)
            while True:
                rows = cursor.fetchmany(10000)
                if not rows:
                    break

                for row in rows:
                    upddata += 1
                    histtable.scdensure(row)

        if CONFIG.simulate:
            pygramcon.rollback()
        else:
            pygramcon.commit()

        pygramcon.close()
        tsstr = time.strftime("%H:%M:%S", time.gmtime(time.time() - t0))
        LOG.info("Updated historic table. {u} rows updated in {t}.".format(u=upddata, t=tsstr))
        with self.__lock:
            self.__updated_hist.value = upddata

    def _migrate_insert_new_data_reg(self):
        t0 = time.time()
        pgconn = psycopg2.connect(self.__db_dsn,
                                  application_name="SimpleETL Insert writer {s}.{t}".format(s=self.__facttable.schema,
                                                                                            t=self.__facttable.table))
        keycols = self.__facttable._get_cols(only_lookupatts=True)
        allcols = self.__facttable._get_cols(include_lookupatts=True, include_ignorecols=True,
                                             include_changeatts=True)
        selcols = []
        for c in allcols:
            selcols.append("a." + quote(c, pgconn))

        existcheck = []
        for c in keycols:
            existcheck.append('a.{col} = b.{col}'.format(col=quote(c, pgconn)))
        delcheck = ""

        if self.__facttable.key_in_atts:  # Primary Key part of attributes
            inscols = allcols.copy()
        else:
            id = _get_nextid(pgconn, self.__facttable.schema, self.__facttable.table, self.__facttable.key)
            selcols = ["row_number() OVER ()+{maxid}".format(maxid=id)] + selcols
            inscols = [self.__facttable.key] + allcols

        insertsql = """INSERT INTO {schema}.{table} ({inscols}) 
                SELECT {selcols}
                FROM tmp_data.{tmptable} a"""
        if keycols:
            insertsql += " WHERE NOT EXISTS (SELECT 1 FROM {schema}.{table} b WHERE\n ({existcheck})) "
        isql = insertsql.format(schema=quote(self.__facttable.schema, pgconn),
                                table=quote(self.__facttable.table, pgconn),
                                inscols=", ".join(quotelist(inscols, pgconn)),
                                selcols=", ".join(selcols),
                                tmptable=quote(self.__facttable.tmptable, pgconn),
                                existcheck=" AND ".join(existcheck),
                                delcheck=delcheck)

        if CONFIG.debug:
            LOG.debug("Test insert query:\n" + isql)

        with pgconn.cursor() as cursor:
            cursor.execute(isql)
            dataloaded = cursor.rowcount

        if CONFIG.simulate:
            pgconn.rollback()
        else:
            pgconn.commit()
        pgconn.close()
        tsstr = time.strftime("%H:%M:%S", time.gmtime(time.time() - t0))
        LOG.info("Inserted into fact table. {i} rows inserted in {t}.".format(i=dataloaded, t=tsstr))
        with self.__lock:
            self.__inserted_reg.value = dataloaded

    def _migrate_insert_new_data_hist(self):
        t0 = time.time()
        pgconn_reader = psycopg2.connect(self.__db_dsn,
                                         application_name="SimpleETL Insert Historic reader {s}.{t}".format(
                                             s=self.__facttable.schema,
                                             t=self.__facttable.table))

        pgconn = psycopg2.connect(self.__db_dsn,
                                  application_name="SimpleETL Insert Historic writer {s}.{t}".format(
                                      s=self.__facttable.schema,
                                      t=self.__facttable.table))
        pygramcon = ConnectionWrapper(pgconn)
        # Separate connections for reading/writing. We need to commit the write connection before read cursor is done.
        keycols = self.__facttable._get_cols(only_lookupatts=True)

        measurecols = self.__facttable._get_cols(include_lookupatts=False, include_ignorecols=True,
                                                 include_changeatts=False)
        histwhere = []
        for c in keycols:
            histwhere.append('a.{col} = b.{col}'.format(col=quote(c, pgconn)))

        hist = _get_bulkhisttable(pygramcon, self.__facttable.schema, self.__facttable.table,
                                  self.__facttable.table_historic, keycols, measurecols,
                                  self.__facttable.key, self.__facttable.key)

        newdata = """SELECT a.* from tmp_data.{tmptable} a
                    WHERE NOT EXISTS (SELECT 1 FROM {schema}.{histtable} b
                        WHERE ({existcheck}))

                    """.format(schema=quote(self.__facttable.schema, pgconn),
                               table=quote(self.__facttable.table, pgconn),
                               tmptable=quote(self.__facttable.tmptable, pgconn),
                               histtable=quote(self.__facttable.table_historic, pgconn),
                               existcheck=" AND ".join(histwhere))
        if CONFIG.debug:
            LOG.debug("SQL for inserting new data into historic table:\n" + newdata)

        dataloaded = 0

        id = _get_nextid(pgconn, self.__facttable.schema, self.__facttable.table_historic, self.__facttable.key)
        if CONFIG.debug:
            LOG.debug("Next primary key ID for historic table fact is: " + str(id))
        with pgconn_reader.cursor("New data", cursor_factory=RealDictCursor) as cursor:
            cursor.execute(newdata)
            while True:
                rows = cursor.fetchmany(10000)
                if not rows:
                    break
                for row in rows:

                    dataloaded += 1
                    """
                    for k, v in list(row.items()):
                        if isinstance(v, str):
                            row[k] = v.replace("\t", "\\t").replace("\n", "\\n").replace("\r", "\\r")
                        if isinstance(v, dict):
                            row[k] = json.dumps(v).replace('\\', '\\\\')
                    """
                    row["_validfrom"] = self.__data_timestamp
                    row["_validto"] = None
                    row["_version"] = 1
                    row[self.__facttable.key] = id
                    id += 1
                    # print(row)
                    hist.insert(row)
                    if dataloaded % 100000 == 0:
                        LOG.info("Historic table mid-way commit: " + str(dataloaded))
                        if CONFIG.simulate:
                            pygramcon.rollback()
                        else:
                            pygramcon.commit()
        pgconn_reader.close()

        if CONFIG.simulate:
            pygramcon.rollback()
        else:
            pygramcon.commit()
        pygramcon.close()
        tsstr = time.strftime("%H:%M:%S", time.gmtime(time.time() - t0))
        LOG.info("Inserted into historic table. {i} rows inserted in {t}.".format(i=dataloaded, t=tsstr))
        with self.__lock:
            self.__inserted_hist.value = dataloaded

    def _propagate_deleted_data_reg(self):
        t0 = time.time()
        if self.__facttable.deleted_rows_method is None:
            return

        pgconn = psycopg2.connect(self.__db_dsn,
                                  application_name="SimpleETL Delete worker {s}.{t}".format(s=self.__facttable.schema,
                                                                                            t=self.__facttable.table))
        keycols = self.__facttable._get_cols(only_lookupatts=True)

        histwhere = []
        for c in keycols:
            histwhere.append('a.{col} = b.{col}'.format(col=quote(c, pgconn)))
        test = ""

        if self.__facttable.deleted_rows_method == "mark":
            test += " AND a._deleted IS NULL "
        if self.__facttable.handle_deleted_rows_func:
            test += " AND " + self.__facttable.handle_deleted_rows_func()
        deldata = """SELECT a.{key} from {schema}.{table} a
                            WHERE NOT EXISTS (SELECT 1 FROM tmp_data.{tmptable} b
                                WHERE ({existcheck}))

                        {test}

                            """.format(schema=self.__facttable.schema,
                                       key=quote(self.__facttable.key, pgconn),
                                       keycols=", ".join(keycols),
                                       table=quote(self.__facttable.table, pgconn),
                                       tmptable=quote(self.__facttable.tmptable, pgconn),
                                       existcheck=" AND ".join(histwhere),
                                       test=test)
        if CONFIG.debug:
            LOG.debug("SQL for finding deleted rows from regular table:\n" + deldata)

        if self.__facttable.deleted_rows_method == "mark":
            upd = ""
            if self.__facttable.track_last_updated:
                upd = ",_updated='{dk}'"
            maintbl = """UPDATE {sch}."{table}" SET _deleted='{dk}'""" + upd + """ where {key}=%s"""
        elif self.__facttable.deleted_rows_method in ("wipe", "date"):
            maintbl = 'DELETE FROM {sch}."{table}" CASCADE where {key}=%s'
        maintbl = maintbl.format(sch=self.__facttable.schema,
                                 table=self.__facttable.table,
                                 key=self.__facttable.key,
                                 dk=self.__data_timestamp)
        removed = 0

        with pgconn.cursor("Deleted data", cursor_factory=RealDictCursor) as cursor:
            cursor.execute(deldata)

            while True:
                rows = cursor.fetchmany(10000)
                if not rows:
                    break
                with pgconn.cursor() as cursor2:
                    for row in rows:
                        removed += 1

                        try:
                            if (self.__facttable.deleted_rows_limit is None
                                    or removed < self.__facttable.deleted_rows_limit):
                                cursor2.execute(maintbl, (row[self.__facttable.key],))
                        except psycopg2.IntegrityError as err:
                            LOG.warning(
                                "Could not remove entry due to the user has allready been removed this day:" + str(err))
                            if CONFIG.simulate:
                                pgconn.rollback()
                            else:
                                pgconn.commit()
        if (self.__facttable.deleted_rows_limit is not None
                and removed >= self.__facttable.deleted_rows_limit):
            LOG.error("Too many rows about to be deleted: rows {n} > limit {m}".format(n=removed,
                                                                                       m=self.__facttable.deleted_rows_limit))
            pgconn.rollback()
            self.set_shutdown()
            pgconn.close()
            return

        if CONFIG.simulate:
            pgconn.rollback()
        else:
            pgconn.commit()

        if self.__facttable.deleted_mark_keep_days is not None:
            with pgconn.cursor() as cursor:

                cursor.execute(
                    "DELETE FROM {s}.{t} WHERE _deleted < timezone('UTC', now()) - '{i} days 6 hours'::INTERVAL"
                        .format(s=self.__facttable.schema, t=self.__facttable.table,
                                i=self.__facttable.deleted_mark_keep_days))
            wiped = cursor.rowcount
            LOG.info("{w} rows wiped from fact table. Deleted more than {n} days ago.".format(w=wiped,
                                                                                              n=self.__facttable.deleted_mark_keep_days))
            if CONFIG.simulate:
                pgconn.rollback()
            else:
                pgconn.commit()
        pgconn.close()
        # print("Removed",removed)
        tsstr = time.strftime("%H:%M:%S", time.gmtime(time.time() - t0))
        LOG.info("Removed data from fact table. {r} rows removed in {t}. Method: {m}."
                 .format(r=removed, t=tsstr, m=self.__facttable.deleted_rows_method))
        with self.__lock:
            self.__deleted_reg.value = removed

    def _propagate_deleted_data_hist(self):
        t0 = time.time()
        if self.__facttable.deleted_rows_method is None:
            return

        pgconn = psycopg2.connect(self.__db_dsn,
                                  application_name="SimpleETL Delete worker {s}.{t}".format(s=self.__facttable.schema,
                                                                                            t=self.__facttable.table_historic))
        keycols = self.__facttable._get_cols(only_lookupatts=True)
        histwhere = []
        for c in keycols:
            histwhere.append('a.{col} = b.{col}'.format(col=quote(c, pgconn)))
        test = ""
        if self.__facttable.deleted_rows_method != "wipe":
            # If not wiping, we are only concerned with live data. When wiping we want to remove all live and historic data.
            test = " AND _validto is null "

        if self.__facttable.handle_deleted_rows_func:
            test += " AND " + self.__facttable.handle_deleted_rows_func()
        # factkey = "_" + self.__facttable.table + "_" + self.__facttable.key
        deldata = """SELECT a.{key}--, {keycols} 
                            from {schema}."{histtable}" a
                            WHERE NOT EXISTS (SELECT 1 FROM tmp_data."{tmptable}" b
                                WHERE ({existcheck}))

                        {test}

                            """.format(schema=self.__facttable.schema,
                                       key=self.__facttable.key,
                                       # factkey=factkey,
                                       tmptable=self.__facttable.tmptable,
                                       keycols=", ".join(keycols),
                                       table=self.__facttable.table,
                                       histtable=self.__facttable.table_historic,
                                       existcheck=" AND ".join(histwhere),
                                       test=test)
        if CONFIG.debug:
            LOG.debug("SQL for finding deleted rows from historic table:\n" + deldata)
        # print(deldata)
        # histids = 'SELECT {idkey} FROM {sch}."{histtable}" WHERE {keycheck} order by _version desc'

        if self.__facttable.deleted_rows_method == "wipe":
            histtbl = 'DELETE FROM {sch}."{histtable}" CASCADE where {key}=%s'
        else:
            histtbl = """UPDATE {sch}."{histtable}" SET _validto='{dk}' where {key}=%s"""
        histtbl = histtbl.format(
            sch=self.__facttable.schema,
            # table=self.__facttable.table,
            # factkey=factkey,
            histtable=self.__facttable.table_historic,
            dk=self.__data_timestamp,
            key=self.__facttable.key)

        removed = 0
        with pgconn.cursor("Delete historic data", cursor_factory=RealDictCursor) as cursor:
            cursor.execute(deldata)

            while True:
                rows = cursor.fetchmany(10000)
                if not rows:
                    break
                with pgconn.cursor() as cursor2:
                    for row in rows:
                        removed += 1
                        # print(q)
                        cursor2.execute(histtbl, (row[self.__facttable.key],))
        if self.is_shutdown():
            pgconn.rollback()
            pgconn.close()
            return
        if CONFIG.simulate:
            pgconn.rollback()
        else:
            pgconn.commit()
        pgconn.close()
        tsstr = time.strftime("%H:%M:%S", time.gmtime(time.time() - t0))
        LOG.info("Removed data from historic table. {r} rows removed in {t}. Method: {m}."
                 .format(r=removed, t=tsstr, m=self.__facttable.deleted_rows_method))
        with self.__lock:
            self.__deleted_hist.value = removed
