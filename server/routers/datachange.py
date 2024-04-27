from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from server.db import schemas, crud, database, models
from propelauth_py.user import User

from server.db import schemas
from server.db.dependencies import get_db
from server.main import app

router = APIRouter()
@app.post("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: UUID, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db=db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
