from fastapi import Depends, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from ..users.models import User


__author__ = 'Ricardo'
__version__ = '0.1'


router = APIRouter(prefix='/auth', tags=['Auth'])

@router.post('')
async def auth(data:OAuth2PasswordRequestForm=Depends()):
    """
    This method give us an access token

    :param username: username

    :param password: password
    
    :raise httpexception: 404, It is thrown if user does not exist
    
    :returns: access token with type
    """
    
    user = User.authenticate(data.username, data.password)
    print(user)
    
    return {}

