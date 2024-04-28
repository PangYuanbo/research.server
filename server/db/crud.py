# crud.py
from fastapi import HTTPException
from typing import List
from sqlalchemy.orm import Session
from .model import User, Research, Application
from .schemas import UserCreate, ProfessorUpdate, NonProfessorUpdate, ResearchBase, ResearchCreate, ApplicationSchema, \
    ApplicationCreateSchema
from uuid import UUID, uuid4


def update_user(db: Session, user_id: UUID, user_update: dict):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # 更新用户信息
    for key, value in user_update.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


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


def get_user(db: Session, user_id: UUID):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_research(db: Session, research_create: ResearchCreate):
    db_research = Research(
        id=uuid4(),
        **research_create.dict(exclude_unset=True),
    )
    db.add(db_research)
    db.commit()
    db.refresh(db_research)
    return db_research


def get_research(db: Session, research_id: UUID) -> Research:
    return db.query(Research).filter(Research.id == research_id).first()


def get_researches(db: Session, skip: int = 0, limit: int = 100) -> List[Research]:
    return db.query(Research).offset(skip).limit(limit).all()


def apply_for_research(db, research_id, student_id, description):
    db_application = ApplicationCreateSchema(
        research_id=research_id,
        student_id=student_id,
        status=0,
        letter=description
    )
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application


# database.py
def get_researches_by_professor(db: Session, professor_id: UUID, skip: int, limit: int):
    # 查询指定教授ID的研究项目，并进行分页处理
    researches = db.query(Research).filter(Research.professor_id == professor_id).offset(skip).limit(limit).all()
    return researches
