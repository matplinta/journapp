from sqlalchemy import Column, Table, ForeignKey
from app.db.base_class import Base

association_table = Table('association_note_tag', Base.metadata,
    Column('note_id', ForeignKey('note.id'), primary_key=True),
    Column('tag_id', ForeignKey('tag.id'), primary_key=True)
)