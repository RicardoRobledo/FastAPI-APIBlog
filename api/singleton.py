from peewee import MySQLDatabase

from decouple import config


__author__ = 'Ricardo'
__version__ = '0.1'


class Singleton:
    """
    This class define our database connection
    
    Attributes:
        connection (MySQLDatabase): connection to mysql database
    """


    __connection = None


    @classmethod
    def __make_database_connection(cls):
        """
        This method make our connection in a database
        """
        
        cls.__connection = MySQLDatabase(
            database=config('DB_NAME'),
            user=config('DB_USER'),
            password=config('DB_PASSWORD'),
            host=config('DB_HOST'),
            port=config('DB_PORT', cast=int)
        )
    

    @classmethod
    def get_connection(cls):
        """
        This method returns our connection

        Returns:
            An MySQLDatabase connection object
        """
        
        if cls.__connection is None:
            cls.__make_database_connection()

        return cls.__connection
