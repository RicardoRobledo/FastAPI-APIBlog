from fastapi import APIRouter, HTTPException

from .models import Publication, Comments
from ..users.models import User

from .schemas import PublicationGetResponse, PublicationPostRequest

from typing import List


__author__ = 'Ricardo'
__version__ = '0.1'


publications_router = APIRouter(prefix='/publications/publication', tags=['Publications'])
comments_router = APIRouter(prefix='/comments/comment', tags=['Comments'])


# ---------------------------------------------------
#                    Publications
# ---------------------------------------------------


@publications_router.get('', response_model=List[PublicationGetResponse])
async def get_publications(page:int=1, limit:int=10):
    """
    This method returns all publications

    :param page: page number
    
    :param limit: size of page
    
    :returns: publications found
    """
    
    return [ publication for publication in Publication.select().paginate(page, limit) ]


@publications_router.post('', response_model=PublicationGetResponse)
async def create_publication(publication:PublicationPostRequest):
    """
    This method create a publication

    :param title: title of publication
    
    :param content: body of publication
    
    :param user_id: owner user
    
    :returns: publication made up
    """
    
    user = User.select().where(User.id==publication.user_id)

    if not user.exists():
        raise HTTPException(status_code=401, detail='Owner user not found')
    
    user = user.first()
    
    publication = Publication.create(
        title=publication.title,
        content=publication.content,
        user_id=user.id
    )
    
    return publication


# ---------------------------------------------------
#                      Comments
# ---------------------------------------------------
