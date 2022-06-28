import contextlib
from typing import Any, Iterator, List, Optional
import duckdb
import pandas as pd

class dbEngine(object):
    """
    :param db_uri: URI of SQL database to connect to
    """
    
    def __init__(self,db_uri: str):
        """
        eg.
        > db=dbEngine("test")
        """
        self.db_uri = db_uri
        
    @contextlib.contextmanager
    def _session(self) -> Iterator[duckdb.DuckDBPyConnection]:
        connection: duckdb.DuckDBPyConnection = duckdb.connect(self.db_uri)
        cursor: duckdb.DuckDBPyConnection = connection.cursor()
        try:
            yield cursor
            connection.commit()
        finally:
            cursor.close()
            connection.close()

    def sqlprotect(self, inject):
        output = inject
        for n, i in enumerate(inject):
            if i == "'":
                output = output[0:n] + "'" + inject[n:] 
        return output

    def append_df(self, df: str, tbl_name: str):
        df = self.sqlprotect(df)
        tbl_name = self.sqlprotect(tbl_name)
        with self._session() as s:
            s.execute(f"insert into {tbl_name} select * from {df}")
            return True

    def createtbl_from_df(self, df, tblName: str):
        dic = locals()
        tblName = self.sqlprotect(tblName)
        typelkup ={"object":"text", "float64": "float", 'int64' : 'bigint', 'bool': 'boolean'}
        q = f"Create table {tblName} ("
        for col in df.columns:
            typel=df[col].dtype.__str__()
            col = self.sqlprotect(col)
            q += f"{col} {typelkup.get(typel, 'text')}, "
        q = q[:-2]
        q += ")"
        print(q)
        with self._session() as s:
            s.execute(q)
            return True

    def sql(self,sql_script):
        _sql_script = self.sqlprotect(sql_script)
        with self._session() as s:
            df = s.execute(_sql_script).df()
            return df
        
    def create_table(self, **kwargs):
        """
         param kwargs: create arbitrary number of columns inside your table
         param table_name: first parameter must be specified with table_name which creates table
         eg.
         > db.create_table(table_name='store', item='TEXT', quantity='INTEGER', price='REAL')
        """
        query = "CREATE TABLE IF NOT EXISTS {} ("
        comma = r', '
        for key, value in kwargs.items():
            if key != 'table_name':
                query = query + key + ' ' + value + comma
        query = query.format(kwargs['table_name']).rstrip(' ,') + ")"
        with self._session() as s:
            s.execute(query)
            return True
        
    def insert_values(self, *args):
        """
        eg.
        > db.insert_values('store', 'wine glass', 8, 10.5)
        """
        query = r"INSERT INTO {} VALUES ("
        comma = r','
        for arg in args:
            if arg != args[0]:
                if type(arg) == str:
                    query = query + "'" + arg + "'" + comma
                else:
                    query = query + str(arg) + comma
        query = query.format(args[0]).rstrip(" ,") + ")"
        with self._session() as s:
            s.execute(query)
            return True
    
    def view(self, table_name):
        """
        eg.
        > db.view('store')
        """
        query = "SELECT * FROM {}".format(table_name)
        with self._session() as s:
            df = s.execute(query).df()
            return df


    def delete_specific_row(self, table_name, row, item):
        """
        eg.
        > #db.delete_specific_row('store','item', "wine glass")
        """
        query = "DELETE FROM {} WHERE {}='{}'"
        query = query.format(table_name, row, item)
        with self._session() as s:
            s.execute(query)
            return True

    def update_table(self, **kwargs):
        """
        eg.
        db.update_table(table_name='store', quantity=10, price=15, item='coffe cup')
        """
        query = "UPDATE {} SET "
        query_ending = " WHERE {}={}"
        comma = r', '
        for key, value in kwargs.items():
            if key != 'table_name':
                if key != 'item':
                    query = query + str(key) + '=' + str(value) + comma
                else:
                    query = query.format(kwargs['table_name']).rstrip(" ,") + query_ending.format(key,"'" + value+"'")

        with self._session() as s:
            s.execute(query)
            return True
    



#x.createtbl_from_df(df,"df_sf")
#db.sql("show tables")
#x.sql('create table test_1 as select * from df')





