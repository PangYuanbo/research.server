# crud.py
from typing import List
from uuid import UUID, uuid4

from fastapi import HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session

from .model import Users, Research, Application
from .schemas import ResearchCreate, ApplicationCreateSchema


def update_user(db: Session, user_id: UUID, user_update: dict):
    db_user = db.query(Users).filter(Users.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Users not found")

    # 更新用户信息
    for key, value in user_update.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_user(db: Session, user_id: UUID):
    # 创建一个User对象，其中id是由调用者提供的UUID，其他字段保留默认值
    db_user = Users(id=user_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: UUID):
    db_user = db.query(Users).filter(Users.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Users not found")
    db.delete(db_user)
    db.commit()
    return {"message": "Users deleted successfully"}


def get_user(db: Session, user_id: str):
    db_user = db.query(Users).filter(Users.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Users not found")
    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Users).order_by(desc(Users.time)).offset(skip).limit(limit).all()


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
    return db.query(Research).order_by(desc(Research.time)).offset(skip).limit(limit).all()


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


def get_applications(db: Session, skip: int, limit: int):
    # 返回按时间字段倒序排列的申请记录
    return db.query(Application).order_by(desc(Application.time)).offset(skip).limit(limit).all()
