from typing import Optional

from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.note import NoteCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def create_random_note(db: Session, *, author_id: Optional[int] = None) -> models.Note:
    if author_id is None:
        user = create_random_user(db)
        author_id = user.id
    title = random_lower_string()
    description = random_lower_string()
    note_in = NoteCreate(title=title, description=description, id=id)
    return crud.note.create_with_author(db=db, obj_in=note_in, author_id=author_id)
