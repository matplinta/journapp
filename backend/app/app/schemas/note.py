# from __future__ import annotations
from pydantic import BaseModel
from typing import Union, List
from datetime import date
from ..models import ColorEnum

# Shared properties
class NoteBase(BaseModel):
    title: Union[str, None] = None
    contents: str
    start_date: date
    end_date: date
    tags: List["Tag"] = []
    color: ColorEnum = ColorEnum.default
    favourite: bool = False 

# Properties to receive on note creation
class NoteCreate(NoteBase):
    pass


# Properties to receive on note update
class NoteUpdate(NoteBase):
    pass


# Properties shared by models stored in DB
class NoteInDBBase(NoteBase):
    id: int
    author_id: int

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
    notes: List[Note]

# Properties to receive on tag creation
class TagCreate(TagBase):
    notes: List[Note] = []

# Properties to receive on tag update
class TagUpdate(TagBase):
    pass


# Properties shared by models stored in DB
class TagInDBBase(TagBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Tag(TagInDBBase):
    pass


# Properties stored in DB
class TagInDB(TagInDBBase):
    pass


NoteBase.update_forward_refs()
NoteUpdate.update_forward_refs()
NoteCreate.update_forward_refs()
Note.update_forward_refs()
# NoteInDBBase.update_forward_refs()
# NoteInDB.update_forward_refs()