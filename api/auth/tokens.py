import jwt

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from decouple import config

from ..users.models import User

from datetime import timedelta, datetime


__author__ = 'Ricardo'
__vesion__ = '0.1'


sign = config('SECRET_KEY')
oauth2_schema = OAuth2PasswordBearer(tokenUrl='/api/v1/auth')


def generate_access_token(user, days=1):
    
    data = {
        'id': user.id,
        'username': user.username,
        'exp': datetime.utcnow()+timedelta(days=days),
    }
    
    return jwt.encode(data, sign, algorithm="HS256")


def get_token(token):
    try:
        return jwt.decode(token, sign, algorithms=["HS256"])
    except Exception as error:
        return None


def get_user(token:str=Depends(oauth2_schema)):

    data = get_token(token)

    if not data is None:
        return User.select().where(User.id==data['id']).first()
    else:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
            headers={'WWW-Authenticate':'Bearer'}
        )
