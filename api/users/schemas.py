from pydantic import BaseModel

from ..common_schemas import ResponseModel


__author__ = 'Ricardo'
__version__ = '0.1'


class UserRequestModel(BaseModel):
    
    name: str
    username: str
    password: str
    email: str


class UserResponsePostModel(ResponseModel):

    username: str


class UserResponseGetModel(ResponseModel):

    id: int
    username: str
    email: str
    is_active: bool
