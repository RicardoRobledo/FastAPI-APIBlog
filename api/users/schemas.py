from pydantic import BaseModel

from typing import Optional

from ..common_schemas import ResponseModel


__author__ = 'Ricardo'
__version__ = '0.1'


class UserRequestPostModel(BaseModel):
    
    name: str
    username: str
    password: str
    email: str


class UserRequestGetModel(BaseModel):
    
    name: Optional[str]
    username: Optional[str]
    password: Optional[str]
    email: Optional[str]


class UserResponseGetModel(ResponseModel):

    username: str
