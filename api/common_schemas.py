from peewee import ModelSelect

from pydantic.utils import GetterDict

from typing import Any

from pydantic import BaseModel


__author__ = 'Ricardo'
__version__ = '0.1'


class PeeweeGetterDict(GetterDict):

    def get(self, key:Any, default:Any=None):
        
        res = getattr(self._obj, key, default)
        
        if isinstance(res, ModelSelect):
            return list(res)

        return res


class ResponseModel(BaseModel):
    
    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
