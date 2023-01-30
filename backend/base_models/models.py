from pydantic import BaseModel, Field
from typing_extensions import Annotated





# class LinkData(BaseModel):
#     link:list[dict]
#     class Config:
#          orm_mode=True

class backlinkData(BaseModel):
    link:str
    website:str
    

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
    birthday:str
    is_admin:bool = False
    photo:str




