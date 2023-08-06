"Clone of unreleased pygrametl table."

import pygrametl
from pygrametl.tables import Dimension, FIFODict


class SlowlyChangingDimension(Dimension):
    """A class for accessing a slowly changing dimension of "type 2".

       "Type 1" updates can also be applied for a subset of the attributes.

       Caching is used. We assume that the DB doesn't change or add any
       attribute values that are cached.
       For example, a DEFAULT value in the DB or automatic type coercion can
       break this assumption.
    """

    def __init__(self, name, key, attributes, lookupatts, versionatt,
                 fromatt=None, fromfinder=None,
                 toatt=None, tofinder=None, minfrom=None, maxto=None,
                 srcdateatt=None, srcdateparser=pygrametl.ymdparser,
                 type1atts=(), cachesize=10000, prefill=False, idfinder=None,
                 usefetchfirst=False, useorderby=True, targetconnection=None):
        """Arguments:
           - name: the name of the dimension table in the DW
           - key: the name of the primary key in the DW
           - attributes: a sequence of the attribute names in the dimension
             table. Should not include the name of the primary key which is
             given in the key argument, but should include versionatt,
             fromatt, and toatt.
           - lookupatts: a sequence with a subset of the attributes that
             uniquely identify a dimension members. These attributes are thus
             used for looking up members.
           - versionatt: the name of the attribute holding the version number
           - fromatt: the name of the attribute telling from when the version
             becomes valid. Not used if None. Default: None
           - fromfinder: a function(targetconnection, row, namemapping)
             returning a value for the fromatt for a new version (the function
             is first used when it is determined that a new version must be
             added; it is not applied to determine this).
             If fromfinder is None and srcdateatt is also None,
             pygrametl.today is used as fromfinder. If fromfinder is None
             and srcdateatt is not None,
             pygrametl.datereader(srcdateatt, srcdateparser) is used.
             In other words, if no date attribute and no special
             date function are given, new versions get the date of the current
             day. If a date attribute is given (but no date function), the
             date attribute's value is converted (by means of srcdateparser)
             and a new version gets the result of this as the date it is valid
             from. Default: None
           - toatt: the name of the attribute telling until when the version
             is valid. Not used if None. Default: None
           - tofinder: a function(targetconnection, row, namemapping)
             returning a value for the toatt. If not set, fromfinder is used
             (note that if fromfinder is None, it is set to a default
             function -- see the comments about fromfinder. The possibly
             modified value is used here.) Default: None
           - minfrom: the value to use for fromatt for the 1st version of a
             member if fromatt is not already set. If None, the value is
             found in the same way as for other new versions, i.e., as
             described for fromfinder. If fromatt should take the value
             NULL for the 1st version, set minfrom to a tuple holding a single
             element which is None: (None,). Note that minto affects the 1st
             version, not any following versions. Note also that if the member
             to insert already contains a value for fromatt, minfrom is
             ignored.
             Default: None.
           - maxto: the value to use for toatt for new members. Default: None
           - srcdateatt: the name of the attribute in the source data that
             holds a date showing when a version is valid from. The data is
             converted to a datetime by applying srcdateparser on it.
             If not None, the date attribute is also used when comparing
             a potential new version to the newest version in the DB.
             If None, the date fields are not compared. Default: None
           - srcdateparser: a function that takes one argument (a date in the
             format scrdateatt has) and returns a datetime.datetime.
             If srcdateatt is None, srcdateparser is not used.
             Default: pygrametl.ymdparser (i.e., the default value is a
             function that parses a string of the form 'yyyy-MM-dd')
           - type1atts: a sequence of attributes that should have type1 updates
             applied. Default: ()
           - cachesize: the maximum size of the cache. 0 disables caching
             and values smaller than 0 allows unlimited caching
           - prefill: decides if the cache should be prefilled with the newest
             versions. Default: False.
           - idfinder: a function(row, namemapping) -> key value that assigns
             a value to the primary key attribute based on the content of the
             row and namemapping. If not given, it is assumed that the primary
             key is an integer, and the assigned key value is then the current
             maximum plus one.
           - usefetchfirst: a flag deciding if the SQL:2008 FETCH FIRST
             clause is used when prefil is True. Depending on the used DBMS
             and DB driver, this can give significant savings wrt. to time and
             memory. Not all DBMSs support this clause yet. Default: False
           - targetconnection: The ConnectionWrapper to use. If not given,
             the default target connection is used.
           - useorderby: a flag deciding if ORDER BY is used in the SQL to
             select the newest version. If True, the DBMS thus does the
             sorting. If False, all versions are fetched and the highest
             version is found in Python. For some systems, this can lead to
             significant performance improvements. Default: True
        """
        # TODO: Should scdensure just override ensure instead of being a new
        #       method?

        Dimension.__init__(self,
                           name=name,
                           key=key,
                           attributes=attributes,
                           lookupatts=lookupatts,
                           idfinder=idfinder,
                           defaultidvalue=None,
                           rowexpander=None,
                           targetconnection=targetconnection)

        if not versionatt:
            raise ValueError('A version attribute must be given')

        self.versionatt = versionatt
        self.fromatt = fromatt
        if fromfinder is not None:
            self.fromfinder = fromfinder
        elif srcdateatt is not None:  # and fromfinder is None
            self.fromfinder = pygrametl.datereader(srcdateatt, srcdateparser)
        else:  # fromfinder is None and srcdateatt is None
            self.fromfinder = pygrametl.today
        self.toatt = toatt
        if tofinder is None:
            tofinder = self.fromfinder
        self.tofinder = tofinder
        self.minfrom = minfrom
        self.maxto = maxto
        self.srcdateatt = srcdateatt
        self.srcdateparser = srcdateparser
        self.type1atts = type1atts
        self.useorderby = useorderby
        if cachesize > 0:
            self.rowcache = FIFODict(cachesize)
            self.keycache = FIFODict(cachesize)
        elif cachesize < 0:
            self.rowcache = {}
            self.keycache = {}
        # else cachesize == 0 and we do not create any caches
        self.__cachesize = cachesize
        self.__prefill = cachesize and prefill  # no prefilling if no caching

        # Check that versionatt, fromatt and toatt are also declared as
        # attributes
        for var in (versionatt, fromatt, toatt):
            if var and var not in attributes:
                raise ValueError("%s not present in attributes argument" %
                                 (var,))

        # Now extend the SQL from Dimension such that we use the versioning
        self.keylookupsql += " ORDER BY %s DESC" % (self.quote(versionatt),)

        # Now create SQL for looking up the key with a local sort
        # This gives "SELECT key, version FROM name WHERE
        # lookupval1 = %(lookupval1)s AND lookupval2 = %(lookupval2)s AND ..."
        self.keyversionlookupsql = "SELECT " + self.quote(key) + ", " + \
                                   self.quote(versionatt) + " FROM " + name + \
                                   " WHERE " + " AND ".join(["%s = %%(%s)s" % (self.quote(lv), lv)
                                                             for lv in lookupatts])

        if toatt:
            self.updatetodatesql = \
                "UPDATE %s SET %s = %%(%s)s WHERE %s = %%(%s)s" % \
                (name, self.quote(toatt), toatt, self.quote(key), key)

        if self.__prefill:
            self.__prefillcaches(usefetchfirst)

    def __prefillcaches(self, usefetchfirst):
        args = None
        if self.toatt:
            # We can use the toatt to see if rows are still current.
            # Select all attributes from the rows where maxto is set to the
            # default value (which may be NULL)
            sql = 'SELECT %s FROM %s WHERE %s %s' % \
                  (', '.join(self.quotelist(self.all)), self.name,
                   self.quote(self.toatt),
                   self.maxto is None and 'IS NULL' or '= %(maxto)s')
            if self.maxto is not None:
                args = {'maxto': self.maxto}
        else:
            # We have to find max(versionatt) for each group of lookupatts and
            # do a join to get the right rows.
            lookupattlist = ', '.join(self.lookupatts)
            newestversions = ('SELECT %s, MAX(%s) AS %s FROM %s GROUP BY %s' %
                              (self.quote(lookupattlist),
                               self.quotelist(self.versionatt),
                               self.quotelist(self.versionatt), self.name,
                               self.quotelist(lookupattlist)))
            joincond = ' AND '.join(['A.%s = B.%s' % (self.quote(att), att)
                                     for att in [l for l in self.lookupatts] +
                                     [self.versionatt]
                                     ])
            sql = 'SELECT %s FROM (%s) AS A, %s AS B WHERE %s' % \
                  (', '.join(['B.%s AS %s' % (self.quote(att), att)
                              for att in self.all]),
                   newestversions, self.name, joincond)

        # sql is a statement that fetches the newest versions from the database
        # in order to fill the caches, the FETCH FIRST clause is for a finite
        # cache, if the user set the flag that it is supported by the database.
        positions = [self.all.index(att) for att in self.lookupatts]
        if self.__cachesize > 0 and usefetchfirst:
            sql += ' FETCH FIRST %d ROWS ONLY' % self.__cachesize
        self.targetconnection.execute(sql, args)

        if self.__cachesize < 0:
            allrawrows = self.targetconnection.fetchalltuples()
        else:
            allrawrows = self.targetconnection.fetchmanytuples(
                self.__cachesize)

        for rawrow in allrawrows:
            self.rowcache[rawrow[0]] = rawrow
            t = tuple([rawrow[i] for i in positions])
            self.keycache[t] = rawrow[0]

    def lookup(self, row, namemapping={}):
        """Find the key for the newest version with the given values.

           Arguments:
           - row: a dict which must contain at least the lookup attributes
           - namemapping: an optional namemapping (see module's documentation)
        """
        if self.__prefill and (self.__cachesize < 0 or
                               len(self.keycache) < self.__cachesize):
            # Everything is cached. We don't have to look in the DB
            return self._before_lookup(row, namemapping)
        else:
            # Something is not cached so we have to use the classical lookup.
            # Note that __init__ updated self.keylookupsql to use ORDER BY ...
            if self.useorderby:
                return Dimension.lookup(self, row, namemapping)
            else:
                return self.__lookupnewestlocally(row, namemapping)

    def __lookupnewestlocally(self, row, namemapping):
        """Find the key for the newest version of the row with the given values.

           Arguments:
           - row: a dict which must contain at least the lookup attributes
           - namemapping: an optional namemapping (see module's documentation)
        """
        # Based on Dimension.lookup, but uses keyversionlookupsql and
        # finds the newest version locally (no sorting on the DBMS)
        key = self._before_lookup(row, namemapping)
        if key is not None:
            return key

        self.targetconnection.execute(self.keyversionlookupsql, row,
                                      namemapping)

        versions = [kv for kv in self.targetconnection.fetchalltuples()]
        if not versions:
            # There is no existing version
            keyvalue = None
        else:
            # Look in all (key, version) pairs and find the key for the newest
            # version
            keyvalue, versionvalue = versions[-1]
            for kv in versions:
                if kv[1] > versionvalue:
                    keyvalue, versionvalue = kv

        self._after_lookup(row, namemapping, keyvalue)
        return keyvalue

    def scdensure(self, row, namemapping={}):
        """Lookup or insert a version of a slowly changing dimension member.

           .. Note:: Has side-effects on the given row.

           Arguments:
           - row: a dict containing the attributes for the member.
             key, versionatt, fromatt, and toatt are not required to be
             present but will be added (if defined).
           - namemapping: an optional namemapping (see module's documentation)
        """
        versionatt = (namemapping.get(self.versionatt) or self.versionatt)
        key = (namemapping.get(self.key) or self.key)
        if self.fromatt:  # this protects us against None in namemapping.
            fromatt = (namemapping.get(self.fromatt) or self.fromatt)
        else:
            fromatt = None
        if self.toatt:
            toatt = (namemapping.get(self.toatt) or self.toatt)
        else:
            toatt = None
        if self.srcdateatt:
            srcdateatt = (namemapping.get(self.srcdateatt) or self.srcdateatt)
        else:
            srcdateatt = None

        # Get the newest version and compare to that
        keyval = self.lookup(row, namemapping)

        if keyval is None:
            # It is a new member. We add the first version.
            row[versionatt] = 1
            if fromatt and fromatt not in row:
                if self.minfrom is not None:
                    # We need the following hack to distinguish between
                    # 'not set' and 'use the value None'...
                    if self.minfrom == (None,):
                        row[fromatt] = None
                    else:
                        row[fromatt] = self.minfrom
                else:
                    row[fromatt] = self.fromfinder(self.targetconnection,
                                                   row, namemapping)
            if toatt and toatt not in row:
                row[toatt] = self.maxto
            row[key] = self.insert(row, namemapping)
            return row[key]
        else:
            # There is an existing version. Check if the attributes are
            # identical
            type1updates = {}  # for type 1
            addnewversion = False  # for type 2
            other = self.getbykey(keyval)  # the full existing version
            for att in self.all:
                # Special (non-)handling of versioning and key attributes:
                if att in (self.key, self.versionatt):
                    # Don't compare these - we don't expect them to have
                    # meaningful values in row
                    continue
                # We may have to compare the "from dates"
                elif att == self.toatt:
                    if other[self.toatt] != self.maxto:
                        addnewversion = True

                elif att == self.fromatt:
                    if self.srcdateatt is None:  # We don't compare dates then
                        continue
                    else:
                        # We have to compare the dates in row[..] and other[..]
                        # We have to make sure that the dates are of comparable
                        # types.
                        rdt = self.srcdateparser(row[srcdateatt])
                        if rdt == other[self.fromatt]:
                            continue  # no change in the "from attribute"
                        elif isinstance(rdt, type(other[self.fromatt])):
                            # they are not equal but are of the same type, so
                            # we are dealing with a new date
                            addnewversion = True
                        else:
                            # They have different types (and are thus not
                            # equal). Try to convert to strings and see if they
                            # are equal.
                            modref = (self.targetconnection
                                      .getunderlyingmodule())
                            rowdate = modref.Date(rdt.year, rdt.month, rdt.day)
                            if str(rowdate).strip('\'"') != \
                                    str(other[self.fromatt]).strip('\'"'):
                                addnewversion = True
                # Handling of "normal" attributes:
                else:
                    mapped = (namemapping.get(att) or att)
                    if row[mapped] != other[att]:
                        if att in self.type1atts:
                            type1updates[att] = row[mapped]
                        else:
                            addnewversion = True
                if addnewversion and not self.type1atts:
                    # We don't have to look for possible type 1 updates
                    # and we already know that a type 2 update is needed.
                    break
                # else: continue

            if len(type1updates) > 0:
                # Some type 1 updates were found
                self.__performtype1updates(type1updates, other)

            if addnewversion:  # type 2
                # Make a new row version and insert it
                row.pop(key, None)
                row[versionatt] = other[self.versionatt] + 1
                if fromatt:
                    row[fromatt] = self.fromfinder(self.targetconnection,
                                                   row, namemapping)
                if toatt:
                    row[toatt] = self.maxto
                row[key] = self.insert(row, namemapping)
                # Update the todate attribute in the old row version in the DB.
                if toatt:
                    toattval = self.tofinder(self.targetconnection, row,
                                             namemapping)
                    self.targetconnection.execute(
                        self.updatetodatesql, {
                            self.key: keyval, self.toatt: toattval})
                # Only cache the newest version
                if self.__cachesize and keyval in self.rowcache:
                    del self.rowcache[keyval]
            else:
                # Update the row dict by giving version and dates and the key
                row[key] = keyval
                row[versionatt] = other[self.versionatt]
                if self.fromatt:
                    row[fromatt] = other[self.fromatt]
                if self.toatt:
                    row[toatt] = other[self.toatt]

            return row[key]

    def _before_lookup(self, row, namemapping):
        if self.__cachesize:
            namesinrow = [(namemapping.get(a) or a) for a in self.lookupatts]
            searchtuple = tuple([row[n] for n in namesinrow])
            return self.keycache.get(searchtuple, None)
        return None

    def _after_lookup(self, row, namemapping, resultkey):
        if self.__cachesize and resultkey is not None:
            namesinrow = [(namemapping.get(a) or a) for a in self.lookupatts]
            searchtuple = tuple([row[n] for n in namesinrow])
            self.keycache[searchtuple] = resultkey

    def _before_getbykey(self, keyvalue):
        if self.__cachesize:
            res = self.rowcache.get(keyvalue)
            if res is not None:
                return dict(zip(self.all, res))
        return None

    def _after_getbykey(self, keyvalue, resultrow):
        if self.__cachesize and resultrow[self.key] is not None:
            # if resultrow[self.key] is None, no result was found in the db
            self.rowcache[keyvalue] = tuple([resultrow[a] for a in self.all])

    def _before_update(self, row, namemapping):
        """ """
        # We have to remove old values from the caches.
        key = (namemapping.get(self.key) or self.key)
        for att in self.lookupatts:
            if (att in namemapping and namemapping[att] in row) or att in row:
                # A lookup attribute is about to be changed and we should make
                # sure that the cache does not map from the old value.  Here,
                # we can only see the new value, but we can get the old lookup
                # values by means of the key:
                oldrow = self.getbykey(row[key])
                searchtuple = tuple([oldrow[n] for n in self.lookupatts])
                if searchtuple in self.keycache:
                    del self.keycache[searchtuple]
                break

        if row[key] in self.rowcache:
            # The cached row is now incorrect. We must make sure it is
            # not in the cache.
            del self.rowcache[row[key]]

        return None

    def _after_insert(self, row, namemapping, newkeyvalue):
        """ """
        # After the insert, we can look it up. Pretend that we
        # did that. Then we get the new data cached.
        # NB: Here we assume that the DB doesn't change or add anything.
        # For example, a DEFAULT value in the DB or automatic type coercion can
        # break this assumption.
        # Note that we always cache inserted members (in CachedDimension
        # this is an option).
        if self.__cachesize:
            self._after_lookup(row, namemapping, newkeyvalue)
            tmp = pygrametl.project(self.all[1:], row, namemapping)
            tmp[self.key] = newkeyvalue
            self._after_getbykey(newkeyvalue, tmp)

    def __performtype1updates(self, updates, lookupvalues, namemapping={}):
        """ """
        # find the keys in the rows that should be updated
        self.targetconnection.execute(self.keylookupsql, lookupvalues,
                                      namemapping)
        updatekeys = [e[0] for e in self.targetconnection.fetchalltuples()]
        updatekeys.reverse()
        # Generate SQL for the update
        valparts = ", ".join(
            ["%s = %%(%s)s" % (self.quote(k), k) for k in updates])
        keyparts = ", ".join([str(k) for k in updatekeys])
        sql = "UPDATE %s SET %s WHERE %s IN (%s)" % \
              (self.name, valparts, self.quote(self.key), keyparts)
        self.targetconnection.execute(sql, updates)
        # Remove from our own cache
        for key in updatekeys:
            if key in self.rowcache:
                del self.rowcache[key]
