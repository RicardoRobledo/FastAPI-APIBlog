from fastapi import APIRouter, HTTPException, Depends

from ..auth.tokens import get_user

from .models import Publication, Comment
from ..users.models import User

from .schemas import (
    PublicationGetResponse,
    PublicationPostRequest,
    PublicationSpecificGetResponse,
    CommentGetResponse,
    CommentPostRequest,
    CommentPutRequest
)

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
async def create_publication(publication:PublicationPostRequest, user:User=Depends(get_user)):
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
async def delete_publication(publication_id:int, user:User=Depends(get_user)):
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
    
    print(type(publication.user_id.id))
    print(type(user.id))

    if publication.user_id.id!=user.id:
        raise HTTPException(status_code=300, detail='You are not the owner')

    publication.is_active = False
    publication.save()
    
    return publication


# ---------------------------------------------------
#                      Comments
# ---------------------------------------------------


@comments_router.get('', response_model=List[CommentGetResponse])
async def get_comments(page:int=1, limit:int=10):
    """
    This method give us all comments
    
    :param page: page number
    
    :param limit: comments quantity to show
    
    :return: comments gotten
    """

    return [ comment for comment in Comment.select().paginate(page, limit) ]


@comments_router.get('/{comment_id}', response_model=CommentGetResponse)
async def get_comment(comment_id:int):
    """
    This method give us a comment
    
    :param comment_id: Comment's identifier
    
    :raise httpexception: 401, It is thrown if comment_id does not exists
    
    :return: comment gotten
    """
    
    comment = Comment.select().where((Comment.id==comment_id)&(Comment.is_active))
    
    if not comment.exists():
        raise HTTPException(detail='Comment not found', status_code=401)

    return comment.first()



@comments_router.post('', response_model=CommentGetResponse)
async def create_comment(comment:CommentPostRequest):
    """
    This method make an user up

    :param content: body of our comment
    
    :param publication_id: Publication's identifier
    
    :param user_id: User's identifier
    
    :raise httpexception: 401, It is thrown if publication_id or user_id do not exist
    
    :returns: comment created
    """
    
    if not Publication.select().where((Publication.id==comment.publication_id)&(Publication.is_active)).exists():
        raise HTTPException(detail='Publication not found', status_code=404)

    if not User.select().where((User.id==comment.user_id)&(User.is_active)).exists():
        raise HTTPException(detail='User not found', status_code=404)    
    
    comment = Comment.create(
        content=comment.content,
        publication_id=comment.publication_id,
        user_id=comment.user_id
    )
    
    return comment


@comments_router.put('/{comment_id}', response_model=CommentGetResponse)
async def update_comment(comment_id:int, new_comment:CommentPutRequest):
    """
    This method update a comment given

    :param content: body of our comment
    
    :raise httpexception: 401, It is thrown if comment_id or user_id do not exist
    
    :returns: comment updated
    """

    comment = Comment.select().where((Comment.id==comment_id)&(Comment.is_active))
    
    if not comment.exists():
        raise HTTPException(detail='Comment not found', status_code=401)

    comment = comment.first()
    comment.content = new_comment.content 
    comment.save()

    return comment


@comments_router.delete('/{comment_id}')
async def delete_comment(comment_id):
    """
    This method delete a comment given
    
    :param comment_id: Comment's identifier
    
    :raise httpexception: 401, It is thrown if comment_id does not exist
    
    :returns: comment deleted
    """
    
    comment = Comment.select().where((Comment.id==comment_id)&(Comment.is_active))
    
    if comment.exists():
        HTTPException(status_code=401, detail='That comment does not exist')
    
    comment = comment.first()
    comment.is_active = False
    comment.save()
    
    return comment
