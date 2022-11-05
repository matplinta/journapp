from typing import Any, List, Union
import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import Required
from fastapi.encoders import jsonable_encoder

from app import crud, models, schemas
from app.api import deps


router = APIRouter()


@router.get("/", response_model=List[schemas.Note])
def read_notes(
    db: Session = Depends(deps.get_db),
    tag: Union[list[str], None] = Query(default=None),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve notes.
    """
    if crud.user.is_superuser(current_user):
        notes = crud.note.get_multi(db, skip=skip, limit=limit)
    else:
        if tag:
            notes = crud.note.get_multi_by_author_and_tags(
                db=db, author_id=current_user.id, tags=tag, skip=skip, limit=limit
            )
        else:
            notes = crud.note.get_multi_by_author(
                db=db, author_id=current_user.id, skip=skip, limit=limit
            )
    return notes


@router.get("/listing", response_model=List[schemas.NoteListed])
def read_notes_listing(
    db: Session = Depends(deps.get_db),
    tag: Union[list[str], None] = Query(default=None),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve notes.
    """
    if crud.user.is_superuser(current_user):
        notes = crud.note.get_multi(db, skip=skip, limit=limit)
    else:
        if tag:
            notes = crud.note.get_multi_by_author_and_tags(
                db=db, author_id=current_user.id, tags=tag, skip=skip, limit=limit
            )
        else:
            notes = crud.note.get_multi_by_author(
                db=db, author_id=current_user.id, skip=skip, limit=limit
            )
    return notes


@router.get("/listing/favourites", response_model=List[schemas.NoteListed])
def read_notes_listing_favourites(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve notes.
    """
    return crud.note.get_multi_favourites_by_author(
        db=db, author_id=current_user.id, skip=skip, limit=limit
    )


@router.get("/by_date", response_model=List[schemas.Note])
def read_notes_by_date(
    db: Session = Depends(deps.get_db),
    start_date: datetime.date = Query(default=Required),
    end_date: datetime.date = Query(default=Required),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve notes.
    """
    notes = crud.note.get_multi_by_author_and_dates(
        db=db, 
        author_id=current_user.id, 
        start_date=start_date, 
        end_date=end_date,
        skip=skip, 
        limit=limit
    )
    return notes

@router.get("/listing/by_date", response_model=List[schemas.NoteListed])
def read_notes_listing_by_date(
    db: Session = Depends(deps.get_db),
    start_date: datetime.date = Query(default=Required),
    end_date: datetime.date = Query(default=Required),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve notes.
    """
    notes = crud.note.get_multi_by_author_and_dates(
        db=db, 
        author_id=current_user.id, 
        start_date=start_date, 
        end_date=end_date,
        skip=skip, 
        limit=limit
    )
    return notes


@router.get("/listing/dates_filled", response_model=List[str])
def read_notes_listing_dates_filled(
    db: Session = Depends(deps.get_db),
    start_date: datetime.date = Query(default=Required),
    end_date: datetime.date = Query(default=Required),
    skip: int = 0,
    limit: int = 10000,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve notes.
    """
    notes = crud.note.get_multi_by_author_and_dates(
        db=db, 
        author_id=current_user.id, 
        start_date=start_date, 
        end_date=end_date,
        skip=skip, 
        limit=limit
    )
    return list(set([str(note.start_date) for note in notes]))


@router.get("/by_tags", response_model=List[schemas.Note])
def read_notes_by_tags(
    db: Session = Depends(deps.get_db),
    tag: list[str] = Query(default=Required),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve notes.
    """
    notes = crud.note.get_multi_by_author_and_tags(
        db=db, author_id=current_user.id, tags=tag, skip=skip, limit=limit
    )
    return notes


@router.post("/", response_model=schemas.Note)
def create_note(
    *,
    db: Session = Depends(deps.get_db),
    note_in: schemas.NoteCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new note.
    """
    note = crud.note.create_with_author(db=db, obj_in=note_in, author_id=current_user.id)
    return note


@router.put("/{id}", response_model=schemas.Note)
def update_note(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    note_in: schemas.NoteUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an note.
    """
    note = crud.note.get(db=db, id=id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if not crud.user.is_superuser(current_user) and (note.author_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    note = crud.note.update(db=db, db_obj=note, obj_in=note_in)
    return note


@router.patch("/{id}", response_model=schemas.Note)
def partial_update_note(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    note_in: schemas.NotePartialUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an note.
    """
    note = crud.note.get(db=db, id=id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if not crud.user.is_superuser(current_user) and (note.author_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    update_data = note_in.dict(exclude_unset=True)
    # print(note.tags)
    stored_item_model = schemas.Note(**jsonable_encoder(note))
    updated_item = stored_item_model.copy(update=update_data)
    note = crud.note.update(db=db, db_obj=note, obj_in=updated_item)
    return note


@router.get("/{id}", response_model=schemas.Note)
def read_note_by_id(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get note by ID.
    """
    note = crud.note.get(db=db, id=id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if not crud.user.is_superuser(current_user) and (note.author_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return note


@router.delete("/{id}", response_model=schemas.Note)
def delete_note(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an note.
    """
    note = crud.note.get(db=db, id=id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if not crud.user.is_superuser(current_user) and (note.author_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    note = crud.note.remove(db=db, id=id)
    return note
