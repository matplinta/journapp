from pydantic import BaseModel, EmailStr
from typing import Union, List
from .note import Note

# Shared properties
class UserBase(BaseModel):
    email: Union[EmailStr, None] = None
    is_active: Union[bool, None] = True
    is_superuser: bool = False
    full_name: Union[str, None] = None
    notes: List[Note] = []


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Union[str, None] = None


class UserInDBBase(UserBase):
    id: Union[int, None] = None
    
    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
