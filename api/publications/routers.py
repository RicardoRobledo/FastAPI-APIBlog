from fastapi import APIRouter


__author__ = 'Ricardo'
__version__ = '0.1'


publications_router = APIRouter(prefix='/publications/publication', tags=['Publication'])
comments_router = APIRouter(prefix='/comments/comment', tags=['Comment'])


# ---------------------------------------------------
#                    Publications
# ---------------------------------------------------



# ---------------------------------------------------
#                      Comments
# ---------------------------------------------------
