from fastapi import APIRouter, HTTPException

from .schemas import UserRequestModel, UserResponseGetModel, UserResponsePostModel

from .models import User

from typing import List


__author__ = 'Ricardo'
__version__ = '0.1'


router = APIRouter(prefix='/users/user', tags=['Users'])


@router.post('', response_model=UserResponsePostModel)
async def register(user:UserRequestModel):
    """
    This method create our user given

    :param name: name of user

    :param username: nickname
        
    :param password: password of user

    :param email: email of user

    :raises httpexception: 401, It is raised if a user already exists

    :returns: username received
    """
    
    if User.select().where(User.username==User.encrypt_value(user.username)).first():
        raise HTTPException(status_code=401, detail='That username already exists, try again')

    user = User.create(
        name=user.name,
        username=user.username,
        password=user.password,
        email=user.email
    )
    
    return user


@router.get('/{user_id}', response_model=UserResponseGetModel)
async def get_user(user_id:int):
    """
    This method give us a user
    
    :param user_id: user's identifier
    
    :param httpexception: 401, It is thrown is user does not exist
    
    :returns: user matched
    """
    
    user = User.select().where(User.id==user_id).first()
    
    if user is None:
        raise HTTPException(status_code=401, detail='User not found')
    
    return user


@router.get('', response_model=List[UserResponseGetModel])
async def get_users(limit:int=10, page:int=1):
    """
    This method give us users
    
    :param limit: limit of users to return
    
    :param page: number of page

    :returns: users matched
    """
    
    users = User.select().paginate(page, limit)

    return [ user for user in users ]


@router.delete('/{user_id}', response_model=UserResponseGetModel)
async def delete_user(user_id:int):
    """
    This method delete a user
    
    :param user_id: users's identifier
    
    :raise httpexception: 404, It is throwns if user does not exists 
    
    :returns: user deleted
    """
    
    user = User.select().where(User.id==user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    
    user.delete_instance()
    
    return user


@router.put('/{user_id}', response_model=UserResponseGetModel)
async def update_user(user_id:int, new_user:UserRequestModel):
    """
    This method update a user
    
    :param user_id: users's identifier
    
    :raise httpexception: 404, It is throwns if user does not exists 
    
    :returns: user updated
    """
    
    user = User.select().where(User.id==user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    
    for key, value in vars(new_user).items():
        setattr(user, key, User.encrypt_value(value))

    user.save()

    return user
