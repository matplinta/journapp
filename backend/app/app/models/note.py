from typing import TYPE_CHECKING

from sqlalchemy import Column, Table, ForeignKey, Integer, String, Boolean, Date, Enum
from sqlalchemy.orm import relationship
from .color import ColorEnum
from app.db.base_class import Base
from .association_note_tag import association_table

if TYPE_CHECKING:
    from .user import User  # noqa: F401



class Note(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    contents = Column(String, index=True)
    author_id = Column(Integer, ForeignKey("user.id"))
    author = relationship("User", back_populates="notes")
    tags = relationship("Tag", secondary=association_table ,back_populates="notes")
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    color = Column(Enum(ColorEnum), default=ColorEnum.default)
    favourite = Column(Boolean(), default=False)


