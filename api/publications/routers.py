from fastapi import APIRouter, HTTPException

from .models import Publication, Comments
from ..users.models import User

from .schemas import PublicationGetResponse, PublicationPostRequest, PublicationSpecificGetResponse

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


@publications_router.get('/{publication_id}', response_model=PublicationSpecificGetResponse)
async def get_publications(publication_id:int):
    """
    This method returns a publication given

    :param publication_id: publication's identifier
    
    :raise httpexception: 401, It is thrown if publication is not found
    
    :returns: publication found
    """
    
    publication = Publication.select().where((Publication.id==publication_id) & (Publication.is_active))
    
    if not publication.exists():
        raise HTTPException(status_code=401, detail='Publication not found')
    
    return publication.first()


@publications_router.post('', response_model=PublicationGetResponse)
async def create_publication(publication:PublicationPostRequest):
    """
    This method create a publication

    :param title: title of publication
    
    :param content: body of publication
    
    :param user_id: owner user
    
    :raise httpexception: 401, It is thrown if owner user is not found
    
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


@publications_router.put('/{publication_id}', response_model=PublicationSpecificGetResponse)
async def update_publication(publication_id:int, new_publication:PublicationPostRequest):
    """
    This method update a publication given

    :param publication_id: Publication's identifier
    
    :raise httpexception: 401, It is raised if publication is not found 
    
    :returns: give us our publication updated
    """
    
    publication = Publication.select().where((Publication.id==publication_id)&(Publication.is_active))
    
    if not publication.exists():
        raise HTTPException(status_code=401, detail='Publication not found')
    
    if not User.select().where((User.id==new_publication.user_id)&(User.is_active)).exists():
        raise HTTPException(status_code=401, detail='User not found')
    
    publication = publication.first()

    for key, value in vars(new_publication).items():
        setattr(publication, key, value)

    publication.save()

    return publication


@publications_router.delete('/{publication_id}', response_model=PublicationGetResponse)
async def delete_publication(publication_id:int):
    """
    This method delete a publication given

    :param publication_id: Publication's identifier
    
    :raise httpexception: 401, It is thrown if publication is not found
    
    :returns: publication deleted
    """
    
    publication = Publication.select().where((Publication.id==publication_id) & (Publication.is_active))
    
    if not publication.exists():
        raise HTTPException(status_code=401, detail='Publication not found')
    
    publication = publication.first()
    publication.is_active = False
    publication.save()
    
    return publication


# ---------------------------------------------------
#                      Comments
# ---------------------------------------------------
