from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteUpdate


class CRUDNote(CRUDBase[Note, NoteCreate, NoteUpdate]):
    def create_with_author(
        self, db: Session, *, obj_in: NoteCreate, author_id: int
    ) -> Note:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, author_id=author_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_author(
        self, db: Session, *, author_id: int, skip: int = 0, limit: int = 100
    ) -> List[Note]:
        return (
            db.query(self.model)
            .filter(Note.author_id == author_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


note = CRUDNote(Note)
