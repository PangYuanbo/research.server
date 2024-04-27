from typing import Union
from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy.orm import Session
from propelauth_fastapi import init_auth
import os

from propelauth_py.user import User

from server.db.dependencies import get_db

PROPELAUTH_API_KEY = os.environ.get("PROPELAUTH_API_KEY")
PROPELAUTH_AUTH_URL="https://58121323173.propelauthtest.com"
auth = init_auth(PROPELAUTH_AUTH_URL, PROPELAUTH_API_KEY)


app= FastAPI()

@app.get("/api/whoami")
async def root(current_user: User = Depends(auth.require_user)):
    return {"user_id": f"{current_user.user_id}"}
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.update_user(db=db, user_id=user_id, user=user)

@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user