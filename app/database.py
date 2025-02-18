import mysql.connector
from config import Config
class DatabaseConnection:
    _connection = None
    _config = None
    _cursor = None
    @classmethod
    def get_connection(cls):
        if cls._connection is None or not cls._connection.is_connected():
            cls._connection = mysql.connector.connect(
                host=cls._config['DATABASE_HOST'],
                user=cls._config['DATABASE_USERNAME'],
                port=cls._config['DATABASE_PORT'],
                password=cls._config['DATABASE_PASSWORD'],
                database=cls._config['DATABASE_NAME']
            )
        return cls._connection

    @classmethod
    def set_config(cls, config):
        cls._config = config
    
    @classmethod
    def execute_query(cls, query, params=None):
        conn = cls.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            conn.commit()
        finally:
            cursor.close()
        return cursor

    @classmethod
    def fetch_one(cls, query, params=None):
        cursor = cls.get_connection().cursor()
        cursor.execute(query, params)
        return cursor.fetchone()
    @classmethod
    def fetch_all(cls, query, params=None):
        cursor = cls.get_connection().cursor()
        cursor.execute(query, params)
        return cursor.fetchall()
    @classmethod
    def close_connection(cls):
        if cls._cursor is not None:
            cls._cursor.close()
        if cls._connection is not None:
            cls._connection.close()
            cls._connection = None
