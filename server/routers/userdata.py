from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from db import schemas, crud, database, model

from db.dependencies import get_db
from fastapi import FastAPI

router = APIRouter()


@router.post("/users_create/", response_model=schemas.User)
def create_new_user(user_create: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(db=db, user_create=user_create)
    return db_user


@router.post("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: UUID, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # 判断当前用户是否有教授权限
    if db_user.professor:
        update_data = schemas.ProfessorUpdate(**db_user.__dict__).dict(exclude_unset=True)
    else:
        update_data = schemas.NonProfessorUpdate(**db_user.__dict__).dict(exclude_unset=True)

    updated_user = crud.update_user(db=db, user_id=user_id, user_update=update_data)
    return updated_user


@router.post("/users_delete/{user_id}", status_code=204)
def delete_user_endpoint(user_id: UUID, db: Session = Depends(get_db)):
    return crud.delete_user(db, user_id=user_id)


@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: UUID, db: Session = Depends(get_db)):
    return crud.get_user(db, user_id=user_id)


@router.get("/users/", response_model=List[schemas.User])
def read_users(page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
    skip = (page - 1) * page_size
    limit = page_size
    users = crud.get_users(db, skip=skip, limit=limit)
    return users