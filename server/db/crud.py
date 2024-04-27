# crud.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
from .models import User
from .schemas import UserUpdate, UserCreate
from uuid import UUID, uuid4


def update_user(db: Session, user_id: UUID, user_update: UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        user_data = user_update.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return db_user
    else:
        raise HTTPException(status_code=404, detail="User not found")
def create_user(db: Session, user_create: UserCreate):
    db_user = User(id=uuid4(), **user_create.dict(exclude_unset=True))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
def delete_user(db: Session, user_id: UUID):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}