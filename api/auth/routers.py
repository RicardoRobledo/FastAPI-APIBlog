from fastapi import Depends, status, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from ..users.models import User

from .tokens import generate_access_token


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
    
    if user.exists():
        
        return {
            'token_type': 'Bearer',
            'access_token': generate_access_token(user.first())
        }
        
    else:
        raise HTTPException(
            status_code=401,
            detail='User not found',
            headers={'WWW-Authenticate':'Bearer'}
        )
