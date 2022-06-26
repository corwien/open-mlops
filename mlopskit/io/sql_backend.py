from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator, List, Optional
import duckdb
import random
from pathlib import Path

@contextmanager
def database_connection(dbpath=None) -> Iterator[duckdb.DuckDBPyConnection]:
    if dbpath is None:
        dbpath = f"{Path(__file__).parent}/db.duckdb"
    #else:
    #    dbpath = Path(Path(dbpath).parent, "db")
    connection: duckdb.DuckDBPyConnection = duckdb.connect(dbpath)
    cursor: duckdb.DuckDBPyConnection = connection.cursor()
    try:
        yield cursor
        connection.commit()
    finally:
        cursor.close()
        connection.close()
        
def get_tables(conn):
    'get list of tables in duckdb'
    tables = []
    for table_tuple in conn.execute("PRAGMA show_tables").fetchall():
        tables.append(table_tuple[0])
    return tables


def get_new_table_name(conn):
    'get new name for table which does not exist'
    while True:
        table_name = get_random_table_name()
        if table_name not in get_tables(conn):
            return table_name

def get_random_table_name():
    return 'table_{}'.format(random.randrange(int(1e5), int(1e6)))


def get_new_table_name(conn):
    'get new name for table which does not exist'
    while True:
        table_name = get_random_table_name()
        if table_name not in get_tables(conn):
            return table_name

def save_df(conn, df, name):
    "save dataframe to a duckdb"
    temp_table = get_new_table_name(conn)
    conn.register(temp_table, df)
    sql = "create table {} as select * from {}".format(
        name, temp_table)
    conn.execute(sql)
    conn.unregister(temp_table)
    
def get_df_by_sql(sql,db_path=None,show=True):
    with database_connection(dbpath=db_path) as db:
        if show:
            df = db.execute(sql).df()
        else:
            db.execute(sql)
            df = True
    return df
