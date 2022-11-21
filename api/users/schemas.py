from pydantic import BaseModel, validator

from ..common_schemas import ResponseModel


__author__ = 'Ricardo'
__version__ = '0.1'


class UserRequestModel(BaseModel):
    
    name: str
    username: str
    password: str
    email: str

    
    @validator('username')
    def username_validator(cls, username):
        
        length = len(username)
        
        if length<2 or length>70:
            raise ValueError('Length for username ought to be more than 1 and less than 70 chars')
        
        return username


    @validator('password')
    def password_validator(cls, password):
        
        length = len(password)
        
        if length<1 or length>70:
            raise ValueError('Length for password ought to be more than 1 and less than 70 chars')
        
        return password


class UserResponsePostModel(ResponseModel):

    username: str


class UserResponseGetModel(ResponseModel):

    id: int
    username: str
    email: str
    is_active: bool
