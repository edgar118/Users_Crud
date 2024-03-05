from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel


class login(BaseModel):
    email: Optional[str]=None
    password: Optional[str]=None
    class Config:
        orm_mode = True

class UserInfo(BaseModel):
    name: Optional[str]=None
    age: Optional[int]=None

    class Config:
        orm_mode = True

class User(BaseModel):
    email: Optional[str]=None
    user_info:  Optional[UserInfo]=None
    class Config:
        orm_mode = True

class RequestUser(BaseModel):
    email: Optional[str]=None
    password: Optional[str]=None
    name: Optional[str]=None
    age: Optional[int]=None

class UserList(BaseModel):
    data: List[User] = []