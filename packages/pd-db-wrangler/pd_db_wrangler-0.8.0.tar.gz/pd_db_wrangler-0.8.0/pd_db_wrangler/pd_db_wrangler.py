"""Main module."""
import sqlite3
import pandas as pd
import psycopg2 as pg
import pandas.io.sql as psql


class Pandas_DB_Wrangler:
    """ 
    Helper class for querying databases using pandas.
    It's essential that the CONNECT_STRING be set for
    any of the other functions to work.
    """

    def __init__(self):
        self.CONNECT_STRING = ""
        self.DB_TYPE = ""

    def set_connection_string(self, filename, db_type=""):
        """ 
        Set DB connection string from txt or ini file 
        An example of a Postgres connection might look like: 
        host='127.0.0.1' dbname=db user=user1 password='p@ssW0rD!'
        A sqlite connection is a file path, so it may look like
        '/path/to/sqlite.db'
        db_type must be set in order to use the df_fetch function
        valid db_types presently implemented: 'postgres', 'sqlite'
        """
        self.DB_TYPE = db_type.lower()
        with open(filename, "r") as f:
            self.CONNECT_STRING = f.readline().rstrip()
            return self.CONNECT_STRING

    def read_text_file(self, filename):
        """ Read Text from File """
        with open(filename, "r", encoding='utf-8-sig') as myfile:
            text = myfile.read()
            myfile.close()
        return text

    def read_sql_file(self, filename):
        """ Read SQL from File """
        return self.read_text_file(filename)

    def fetch_from_postgres(self, sql):
        """ 
        Run SQL query on Postgres DB given SQL as a parameter
        """
        cnx = pg.connect(self.CONNECT_STRING)
        df = pd.read_sql(sql, con=cnx)
        cnx.close()
        return df

    def fetch_from_sqlite(self, sql):
        """ Run SQL query on SQLite DB given a db path & SQL """
        cnx = sqlite3.connect(self.CONNECT_STRING)
        df = pd.read_sql_query(sql, con=cnx)
        cnx.close()
        return df

    def df_fetch(self, sql):
        """ 
        Run SQL query on a database with SQL as a parameter
        Please specify connect string and db type using the
        set_connection_string function.
        Valid DB_TYPE values: 'postgres', 'sqlite'
        """
        if self.DB_TYPE == "postgres":
            return self.fetch_from_postgres(sql)
        elif self.DB_TYPE == "sqlite":
            return self.fetch_from_sqlite(sql)
        else:
            return "Please specify db type (e.g. 'postgres', 'sqlite')"
