from psycopg2.extensions import quote_ident

# Functions for quoting SQL identifiers (tables, columns) with ".
# This is necessary if, e.g., columns names include - (dash)
quote = lambda x, pgconn: quote_ident(x, pgconn)
quotelist = lambda x, pgconn: [quote(a, pgconn) for a in x]
