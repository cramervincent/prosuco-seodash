from pydantic import BaseModel, Field
from typing_extensions import Annotated


# class DummyData(BaseModel):
#     title:str
#     author:str
#     description:str
#     rating:int


class LinkData(BaseModel):
    link:list[dict]
    class Config:
         orm_mode=True

class LoginData(BaseModel):
    username:str
    password:str

class ClientRegisterData(BaseModel):
    name:str
    email:str
    password:str

class ClientPatchData(BaseModel):
    name:str
    email:str

class RegisterData(BaseModel):
    firstname:str
    lastname:str
    email:str
    password:str
    birthday:str|None = None
    is_admin:bool = False
    photo:str|None = None




