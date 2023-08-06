SimpleETL - ETL Processing by Simple Specifications
===================================================

SimpleETL er an ETL tool developed by FlexDanmark to easily handling processing of data
from user-defined data sources and automatically generates a dimensionally modelled
data warehouse.

SimpleETL is developed to work with the PostgreSQL DBMS backend with psycopg2 as
database adapter.

Features
--------
- Automatically generates data warehouse dimensional model (star schema)
- Can track changes of facts
- User-defined automatic fact table partitioning
- Handle deleted facts
- Ensures data quality by type and value checking
- Provides a wide range of default data types and allows user to define their own


Installation
------------
SimpleETL can be installed in multiple ways. The simples is to install from pypi::

    $ pip install simpleetl

Dependencies
````````````
SimpleETL requires the psycopg2-binary and the pygrametl package for database
PostgreSQL database connections and table handling.

Example usages
--------------
From the source repository multiple code examples can be found in the examples folder.

A simple example could be:

.. code-block:: python

    from simpleetl import FactTable, runETL, datatypes as dt

    factobj = FactTable(schema="testschema", table="userdata",
                        migrate_updates=True,
                        # Updated to data will be processed. Can be set to False if only appending (will speed things up)
                        store_history=False,  # Create a seperate userdata_historic table for storing changes to facts.
                        track_last_updated=True,
                        # Adds an _updated attribute which keeps track of when data was last updated.
                        lookupatts=["userid"]  # List of attributes uniquely defining a fact
                        )

    factobj.handle_deleted_rows("mark")
    # Tells ETL to mark deleted rows from source with an _deleted timestamp attribute

    factobj.add_column_mapping("userid", dt.bigint, "userid")
    # Map userid from source data to database with same name

    factobj.add_column_mapping("sys_username", dt.text, "username")
    # Rename "sys_username" from source data to "username" in database

    datafeeder = [{"userid": 42, "sys_username": "Jens"}, {"userid": 56, "sys_username": "Svend"}]
    # datafeeder can be a generator or simple a iterable of dictionaries

    stats = runETL(facttable=factobj, datafeeder=datafeeder,
                   db_host="localhost", db_port="5432", db_name="test_db", db_user="dbuser", db_pass="dbpass")


Publications
------------
Ove Andersen, Christian Thomsen, Kristian Torp:
SimpleETL: ETL Processing by Simple Specifications. DOLAP 2018
http://ceur-ws.org/Vol-2062/paper10.pdf