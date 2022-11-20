from pydantic import BaseModel

from ..common_schemas import ResponseModel

from ..users.schemas import UserResponseGetModel


__author__ = 'Ricardo'
__version__ = '0.1'


class PublicationGetResponse(ResponseModel):
    
    title: str
    content: str


class PublicationSpecificGetResponse(ResponseModel):
    
    id: int
    title: str
    content: str
    user_id: UserResponseGetModel
    is_active: bool


class PublicationPostRequest(BaseModel):
    
    title: str
    content: str
    user_id: int
