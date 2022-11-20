from pydantic import BaseModel

from ..common_schemas import ResponseModel


__author__ = 'Ricardo'
__version__ = '0.1'


class PublicationGetResponse(ResponseModel):
    
    title: str
    content: str


class PublicationPostRequest(BaseModel):
    
    title: str
    content: str
    user_id: int
