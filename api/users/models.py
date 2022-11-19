from datetime import datetime

from peewee import(
    Model,
    CharField,
    DateTimeField,
    BooleanField
)

from ..singleton import Singleton


__author__ = 'Ricardo'
__version__ = '0.1'


# -----------------------------------------------
#                       User
# -----------------------------------------------


class User(Model):
    
    username = CharField(max_length=20)
    name = CharField(max_length=20)
    password = CharField(max_length=70)
    email = CharField(max_length=20)
    creation_date = DateTimeField(default=datetime.now)
    is_active = BooleanField(default=True)
    
    def __str__(self):
        return self.username
    
    class Meta:
        database = Singleton.get_connection()
        table_name = 'users'
