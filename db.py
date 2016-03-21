"""
initialize rethink db client
"""

import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError

from constants import *


PROJECT_TABLES = {
    DB_TABLE_CAVILLS: {'keys': set()},
    DB_TABLE_HAIRDOS: {'keys': set()},
    DB_TABLE_POLRUS: {'keys': set()},
    DB_TABLE_USERS: {'keys': set(), 'primary': 'nickname'}}

# Set up db connection client
conn = r.connect(host=DB_HOST, port=DB_PORT)


# Ensure database and tables exists
def db_setup():
    try:
        r.db_create(DB_NAME).run(conn)
        print('Database created.')
    except RqlRuntimeError:
        print('Database already exists.')
    for table, indexes in PROJECT_TABLES.items():
        try:
            if 'primary' in indexes:
                r.db(DB_NAME).table_create(table, primary_key=indexes['primary']).run(conn)
            else:
                r.db(DB_NAME).table_create(table).run(conn)
            print('Table ({table}) creation completed'.format(table=table))
            for index in indexes['keys']:
                r.db(DB_NAME).table(table).index_create(index).run(conn)
                r.db(DB_NAME).table(table).index_wait(index).run(conn)
                print('added index ({index}) on table ({table})'.format(index=index, table=table))
        except RqlRuntimeError:
            print('Table ({table}) already exists.Nothing to do'.format(table=table))


db_setup()
