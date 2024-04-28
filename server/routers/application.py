from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from db import schemas, crud, database, model
from db.dependencies import get_db


router = APIRouter()


@router.post("/research/{research_id}/apply/", response_model=schemas.ResearchBase)
def apply_for_research(
        research_id: UUID,
        student_id: UUID,
        description: str,
        db: Session = Depends(get_db)
):
    """
    Allows a user to apply for a research by appending their user_id to the application column.
    """
    db_research = crud.apply_for_research(db=db, research_id=research_id, student_id=student_id,
                                          description=description)
    if db_research is None:
        raise HTTPException(status_code=404, detail="Research not found")
    return db_research


# accept application
@router.post("/research/{research_id}/accept/", response_model=schemas.ResearchBase)
def accept_application(
        research_id: UUID,
        user_id: UUID,
        db: Session = Depends(get_db)
):
    """
    Determining whether a professor
    :param research_id:
    :param user_id:
    :param db:
    :return:
    """
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.professor:
        """
        Does the professor have this research
        """
        db_research = crud.get_research(db, research_id)
        if db_research is None:
            raise HTTPException(status_code=404, detail="Research not found")
        if db_research.professor_id == db_user.id:
            db_research.status = 1
            db.commit()
            db.refresh(db_research)
            return db_research
        else:
            raise HTTPException(status_code=403, detail="Permission denied,Not the owner of the research")
    else:
        raise HTTPException(status_code=403, detail="Permission denied,Not a professor")


# refused application
@router.post("/research/{research_id}/refused/", response_model=schemas.ResearchBase)
def accept_application(
        research_id: UUID,
        user_id: UUID,
        db: Session = Depends(get_db)
):
    """
    Determining whether a professor
    :param research_id:
    :param user_id:
    :param db:
    :return:
    """
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.professor:
        """
        Does the professor have this research
        """
        db_research = crud.get_research(db, research_id)
        if db_research is None:
            raise HTTPException(status_code=404, detail="Research not found")
        if db_research.professor_id == db_user.id:
            db_research.status = 2
            db.commit()
            db.refresh(db_research)
            return db_research
        else:
            raise HTTPException(status_code=403, detail="Permission denied,Not the owner of the research")
    else:
        raise HTTPException(status_code=403, detail="Permission denied,Not a professor")


@router.get("/applications/", response_model=List[schemas.ApplicationSchema])
def read_applications(
        page: int = Query(1, ge=1, alias="page"),  # ge=1 确保页码不小于1
        page_size: int = Query(10, ge=1, alias="page_size"),  # ge=1 确保每页大小不小于1
        db: Session = Depends(get_db),
):
    # 计算跳过的记录数
    skip = (page - 1) * page_size
    # 查询数据库获取分页数据
    applications = db.query(model.Application).offset(skip).limit(page_size).all()
    return applications

