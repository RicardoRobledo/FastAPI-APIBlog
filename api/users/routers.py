from fastapi import APIRouter, HTTPException

from .schemas import UserRequestModel, UserResponseGetModel, UserResponsePostModel

from .models import User

from typing import List


__author__ = 'Ricardo'
__version__ = '0.1'


router = APIRouter(prefix='/users/user')


@router.post('', response_model=UserResponsePostModel)
async def create_user(user:UserRequestModel):
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


@router.get('', response_model=List[UserResponseGetModel])
async def get_user(limit:int=10, page:int=1):
    """
    This method create our user given

    :param name: name of user

    :param username: nickname

    :param password: password of user

    :param email: email of user

    :raises httpexception: 401, It is raised if a user already exists

    :returns: users matched
    """
    
    users = User.select().paginate(page, limit)

    return [ user for user in users ]
