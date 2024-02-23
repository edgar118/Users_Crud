from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

class User(BaseModel):
    email: Optional[str]=None
    name: Optional[str]=None
    age: Optional[int]=None

    class Config:
        orm_mode = True

class RequestUser(BaseModel):
    email: Optional[str]=None
    password: Optional[str]=None
    name: Optional[str]=None
    age: Optional[int]=None

class UserList(BaseModel):
    data: List[User] = []