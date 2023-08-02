import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from connection import Connection
from base64 import b64encode

class DataBase():

    def __init__(self, dbname:str, connectionsettings:Connection):
        self.username = connectionsettings.username
        self.password = connectionsettings.password
        self.host = connectionsettings.server
        self._database = dbname.lower()
        self._status_handler = None
        self._hashcolumn = "sqlmap_hash"
        self._recreate = True
        self._tables = []

    @property
    def recreate(self) -> bool:
        return self._recreate
    
    @recreate.setter
    def recreate(self, value:bool):
        self._recreate = value

    @property
    def status_handler(self):
        return self._status_handler

    @status_handler.setter
    def status_handler(self, value):
        self._status_handler = value

        
    def _get_cursor(self):
            self._conn = psycopg2.connect(dbname=self._database, user=self.username, password=self.password, host=self.host)
            self._conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT);
            cursor = self._conn.cursor()
            return cursor
                
    def _destroy(self, cursor):
        cursor.close()
        self._conn.close()

    def _execute(self, sentence, values=None):
        try:
            cur = self._get_cursor()
            generated = cur.execute(sentence, values)
            self._conn.commit()
            self._destroy(cur)
            return generated
        except Exception as e:
            print(cur.query.decode('utf-8'))
            raise e
    
    def _select(self, sentence: str, values=None):
        rows = []
        cur = self._get_cursor()
        cur.execute(sentence, values)
        for row in cur.fetchall():
            rows.append(row)
        
        if len(rows)>0:
          return rows
        
        return None

    def _check_exists_db(self, name:str) -> bool:
        sentence = """
                        SELECT datname FROM pg_catalog.pg_database WHERE lower(datname) = lower(%s);
                    """
        db = self._select(sentence, (name,))
        return db is not None

    def _check_exists_table(self, tablename:str) -> bool:
        sentence = """
                        select * from pg_tables where schemaname='public' and tablename=%s
                    """
        db = self._select(sentence, (tablename,))
        return db is not None

    def _check_exists_column(self, tablename:str, columnname:str) ->bool:
        sentence = f"SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = %s  and column_name=%s"
        column = self._select(sentence, (tablename, columnname))
        return column is not None

    def _get_columns(self, tablename:str):
        sentence = f"SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = %s"
        columns = self._select(sentence, (tablename,))
        return columns

    """
    If database exists, drop and create
    """
    def create_database(self, dbname:str):
        if self._recreate:
          self._execute(f'DROP DATABASE IF EXISTS {dbname.lower()}')

        dbexists = self._check_exists_db(dbname)
        if not dbexists:
          create_db = f'CREATE DATABASE "{dbname.lower()}" WITH OWNER={self.username} TEMPLATE template0'
          self._execute(create_db)
        
   
    def create_table(self, name:str, columns=None):
        try:
           dbexists = self._check_exists_db(self._database)
           if dbexists:
               sentence = f"""
                           CREATE TABLE IF NOT EXISTS public.{name}()
                           """
               self._execute(sentence)
               if self._check_exists_table(name):
                 self.create_columns(name, columns)
        except Exception as e:
            raise e

    def _get_columns_from_table(self, tablename:str):
        columns = []
        for t in self._tables:
            if t["table"] == tablename:
                columns = t["columns"]
        
        if len(columns) == 0:
            rows = self._get_columns(tablename)
            columns = [item[0] for item in rows]
            self._tables.append({"table":tablename, "columns":columns})
        
        return columns
    
    def _value_exists(self, tablename:str, hash:str)->bool:
        sentence = f"""
                    Select * from {tablename} where {self._hashcolumn}=%s
                    """
        return not self._select(sentence, (hash,)) is None


    def create_columns(self, tablename:str, columns):
        try:
            if not self._hashcolumn in columns:
                columns.append(self._hashcolumn)

            sentence = f"ALTER TABLE {tablename}\n"

            for index,column in enumerate(columns):
                if not self._check_exists_column(tablename, column):
                    column_type = "TEXT"
                    if column.lower() == self._hashcolumn:
                        column_type = "varchar(50)"

                    sentence += f"ADD COLUMN \"{column.lower()}\" {column_type}"
                    if index != len(columns)-1:
                        sentence+=","
            
            if "COLUMN" in sentence:
              self._execute(sentence)
              if self._hashcolumn in sentence:
                  self._execute(f"CREATE UNIQUE INDEX IF NOT EXISTS {tablename}_{self._hashcolumn}_idx ON public.{tablename} USING btree ({self._hashcolumn})")
        except Exception as e:
            raise e
  
    def insert_data(self, tablename, data):
        try:

            columns = self._get_columns_from_table(tablename)
            parameters = ''
            columns_insert=''
            
            """
            Calculate MD5 for all data
            """
            
            for index, c in enumerate(columns):
                columns_insert+=f'"{c}"'
                if index != len(columns)-1:
                    columns_insert+=','

            for index, column in enumerate(data):
                parameters+="%s"
                if index != len(data)-1:
                    parameters+=","
            
            

            sentence=f"""    
                        INSERT INTO {tablename} ({columns_insert})
                        VALUES ({parameters})
                        ON CONFLICT ({self._hashcolumn}) DO NOTHING
                    """
            self._execute(sentence, data)
        except Exception as e:
            raise e