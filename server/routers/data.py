from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from server.db import schemas, crud, database, models
from propelauth_py.user import User

from server.db import schemas
from server.db.dependencies import get_db
from server.main import app

router = APIRouter()


@app.post("/users_create/", response_model=schemas.User)
def create_new_user(user_create: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(db=db, user_create=user_create)
    return db_user


@app.post("/users_update/{user_id}", response_model=schemas.User)
def update_user(user_id: UUID, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db=db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users_delete/{user_id}", status_code=204)
def delete_user_endpoint(user_id: UUID, db: Session = Depends(get_db)):
    return crud.delete_user(db, user_id=user_id)


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: UUID, db: Session = Depends(get_db)):
    return crud.get_user(db, user_id=user_id)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users
