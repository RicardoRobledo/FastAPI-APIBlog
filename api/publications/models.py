from datetime import datetime

from ..users.models import User

from peewee import(
    BooleanField,
    DateTimeField,
    CharField,
    ForeignKeyField,
    Model
)

from ..singleton import Singleton


__author__ = 'Ricardo'
__version__ = '0.1'


database = Singleton.get_connection()


# -----------------------------------------------
#                   Publication
# -----------------------------------------------


class Publication(Model):
    
    title = CharField(max_length=70)
    content = CharField(max_length=200)
    creation_date = DateTimeField(default=datetime.now)
    is_active = BooleanField(default=True)
    user_id = ForeignKeyField(model=User, backref='user')
    
    class Meta:
        database = database
        table_name = 'publications'


# -----------------------------------------------
#                   Comments
# -----------------------------------------------


class Comments(Model):
    
    content = CharField(max_length=200)
    creation_date = DateTimeField(default=datetime.now)
    is_active = BooleanField(default=True)
    user_id = ForeignKeyField(model=User, backref='user')
    publication_id = ForeignKeyField(model=Publication, backref='publication')
    
    class Meta:
        database = database
        table_name = 'comments'
