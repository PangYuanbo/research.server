import os
from typing import List
from uuid import UUID

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from propelauth_fastapi import init_auth
from propelauth_py.user import User
from sqlalchemy.orm import Session

from ..db import schemas, crud
from ..db.dependencies import get_db

load_dotenv()
router = APIRouter()
AUTH_URL = os.getenv("AUTH_URL")
API_KEY = os.getenv("API_KEY")
auth = init_auth(AUTH_URL, API_KEY)


@router.post("/users_create/", response_model=schemas.Users)
def create_new_user(current_user: User = Depends(auth.require_user), db: Session = Depends(get_db)):
    try:
        db_user = crud.create_user(db=db, user_id=current_user.user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return db_user


@router.post("/users/update")
def update_user(db: Session, user_id: str, user_update: dict):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user:
        for key, value in user_update.items():
            setattr(db_user, key, value)
        db.commit()
        return db_user
    else:
        raise HTTPException(status_code=404, detail="User not found")


@router.post("/users_delete/{user_id}", status_code=204)
def delete_user_endpoint(user_id: UUID, db: Session = Depends(get_db)):
    return crud.delete_user(db, user_id=user_id)


@router.get("/users/{user_id}", response_model=schemas.Users)
def read_user(user_id: UUID, db: Session = Depends(get_db)):
    return crud.get_user(db, user_id=user_id)


@router.get("/users/", response_model=List[schemas.Users])
def read_users(page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
    skip = (page - 1) * page_size
    limit = page_size
    users = crud.get_users(db, skip=skip, limit=limit)
    return users
