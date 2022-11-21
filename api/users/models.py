from datetime import datetime

from peewee import(
    Model,
    CharField,
    DateTimeField,
    BooleanField
)

import hashlib

from ..singleton import Singleton

from .config import ENCRIPTED_FIELDS


__author__ = 'Ricardo'
__version__ = '0.1'


# -----------------------------------------------
#                       User
# -----------------------------------------------


class User(Model):
    
    username = CharField(max_length=70)
    name = CharField(max_length=70)
    password = CharField(max_length=70)
    email = CharField(max_length=70)
    creation_date = DateTimeField(default=datetime.now)
    is_active = BooleanField(default=True)

    
    class Meta:
        database = Singleton.get_connection()
        table_name = 'users'

    
    @classmethod
    def encrypt_value(cls, value):
       
        return hashlib.sha1(value.encode('utf-8')).hexdigest()
    
    
    @classmethod
    def authenticate(cls, username, password):

        user = User.select().where(
            (User.username==cls.encrypt_value(username)) &
            (User.password==cls.encrypt_value(password)) &
            (User.is_active)
        )
       
        return user
    

    @classmethod
    def create(cls, **query):

        for key, value in query.items():
            
            if key in ENCRIPTED_FIELDS:
                query[key] = cls.encrypt_value(value)
       
        return super().create(**query)
