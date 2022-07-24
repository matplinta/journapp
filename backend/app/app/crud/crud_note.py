from typing import List, Union, Dict, Any
import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from app.crud.base import CRUDBase, get_or_create
from app.models.tag import Tag
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteUpdate


class CRUDNote(CRUDBase[Note, NoteCreate, NoteUpdate]):
    def update(
        self,
        db: Session,
        *,
        db_obj: Note,
        obj_in: Union[NoteUpdate, Dict[str, Any]]
    ) -> Note:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        tags_update = update_data.pop("tags", [])

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        tags_list = []
        for tag_data in tags_update:
            tag_instance, _ = get_or_create(db, Tag, **tag_data)
            tags_list.append(tag_instance)
        setattr(db_obj, "tags", tags_list)


        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


    def create_with_author(
        self, db: Session, *, obj_in: NoteCreate, author_id: int
    ) -> Note:
        obj_in_data = jsonable_encoder(obj_in)

        tags_data = obj_in_data.pop('tags', None)
        tags_list = []
        for tag_data in tags_data:
            name = tag_data.pop("name")
            tag_instance, _ = get_or_create(db, Tag, name=name.lower(), **tag_data)
            tags_list.append(tag_instance)
        db_obj = self.model(**obj_in_data, tags=tags_list, author_id=author_id)  # type: ignore
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


    def get_multi_by_author_and_tags(
        self, db: Session, *, author_id: int, tags: list[str], skip: int = 0, limit: int = 100
    ) -> List[Note]:
        results = db.query(Note).filter(Note.author_id == author_id)
        for tag_name in tags:
            results = results.filter(Note.tags.any(name=tag_name))
        return (results.offset(skip).limit(limit).all())


    def get_multi_by_author_and_dates(
        self, db: Session, *, author_id: int, start_date: datetime.date, end_date: datetime.date, skip: int = 0, limit: int = 100
    ) -> List[Note]:
        return (
            db.query(self.model)
            .filter(Note.author_id == author_id)
            .filter(Note.start_date >= start_date)
            .filter(Note.end_date <= end_date)
            .order_by(self.model.start_date.asc(), self.model.end_date.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )


note = CRUDNote(Note)
