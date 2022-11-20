from fastapi import FastAPI, APIRouter

from api.singleton import Singleton

from api.users.models import User

from api.publications.models import Publication, Comment

from api import router as api_v1


__author__ = 'Ricardo'
__version__ = 0.1


app = FastAPI(
    title='Blog API',
    description='In this API we will be able to create publications and comment them',
    version=0.1
)


connection = Singleton.get_connection()


# -----------------------------------------------
#                    Routers
# -----------------------------------------------


app.include_router(api_v1)


# -----------------------------------------------
#                    Events
# -----------------------------------------------


def make_migrations():

    connection.create_tables([User, Publication, Comment])


@app.on_event('startup')
def startup():
    
    print('Server is beggining')
    
    if connection.is_closed():
        connection.connect()
        
        print('Connecting...')

    make_migrations()


@app.on_event('shutdown')
def shutdown():
    
    print('Closing server')
    
    if not connection.is_closed():
        connection.close()
    
    print('Server shut down')
