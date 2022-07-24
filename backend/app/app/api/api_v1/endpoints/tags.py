from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Tag])
def read_tags(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve tags.
    """
    tags = crud.tag.get_multi(db, skip=skip, limit=limit)
    return tags


@router.post("/", response_model=schemas.Tag)
def create_tag(
    *,
    db: Session = Depends(deps.get_db),
    tag_in: schemas.TagCreate,
) -> Any:
    """
    Create new tag.
    """
    tag = crud.tag.create(db=db, obj_in=tag_in)
    return tag


@router.put("/{id}", response_model=schemas.Tag)
def update_tag(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    tag_in: schemas.TagUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an tag.
    """
    tag = crud.tag.get(db=db, id=id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    tag = crud.tag.update(db=db, db_obj=tag, obj_in=tag_in)
    return tag


@router.get("/{id}", response_model=schemas.Tag)
def read_tag(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Get tag by ID.
    """
    tag = crud.tag.get(db=db, id=id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@router.delete("/{id}", response_model=schemas.Tag)
def delete_tag(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Delete an tag.
    """
    tag = crud.tag.get(db=db, id=id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    tag = crud.tag.remove(db=db, id=id)
    return tag
