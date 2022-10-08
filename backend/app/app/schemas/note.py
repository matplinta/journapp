# from __future__ import annotations
from pydantic import BaseModel, validator
from typing import Union, List
from datetime import date
from ..models import ColorEnum

# Shared properties
class NoteBase(BaseModel):
    title: Union[str, None] = None
    start_date: date
    end_date: date
    color: ColorEnum = ColorEnum.default
    favourite: bool = False 

# Properties to receive on note creation
class NoteCreate(NoteBase):
    contents: str
    tags: List["Tag"] = []


# Properties to receive on note update
class NoteUpdate(NoteBase):
    contents: str
    tags: List["Tag"] 


class NotePartialUpdate(BaseModel):
    title: Union[str, None]
    start_date: Union[date, None]
    end_date: Union[date, None]
    color: Union[ColorEnum, None]
    favourite: bool = False
    contents: Union[str, None]
    tags: Union[ List["Tag"], None]

    class Config:
        orm_mode = True


# Properties shared by models stored in DB
class NoteInDBBase(NoteBase):
    id: int
    author_id: int
    contents: str
    tags: List["Tag"]

    class Config:
        orm_mode = True


class NoteListed(NoteBase):
    id: int
    author_id: int
    tags: List["Tag"]

    class Config:
        orm_mode = True


# Properties to return to client
class Note(NoteInDBBase):
    pass


# Properties stored in DB
class NoteInDB(NoteInDBBase):
    pass



# Shared properties
class TagBase(BaseModel):
    name: str

    @validator('name')
    def name_must_be_lowercase(cls, v):
        if not v.islower():
            raise ValueError('name must be lowercase')
        return v

# Properties to receive on tag creation
class TagCreate(TagBase):
    pass
# Properties to receive on tag update
class TagUpdate(TagBase):
    pass


# Properties shared by models stored in DB
class TagInDBBase(TagBase):
    # id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Tag(TagInDBBase):
    # notes: List[Note]
    pass


# Properties stored in DB
class TagInDB(TagInDBBase):
    pass

NoteBase.update_forward_refs()
NoteUpdate.update_forward_refs()
NotePartialUpdate.update_forward_refs()
NoteCreate.update_forward_refs()
NoteListed.update_forward_refs()
Note.update_forward_refs()
# NoteInDBBase.update_forward_refs()
# NoteInDB.update_forward_refs()