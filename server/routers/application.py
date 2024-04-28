from uuid import UUID

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from ..db import schemas, crud, database, model
from ..db.dependencies import get_db
from propelauth_fastapi import init_auth,User
import os
load_dotenv()
AUTH_URL = os.getenv("AUTH_URL")
API_KEY = os.getenv("API_KEY")
auth = init_auth(AUTH_URL, API_KEY)
router = APIRouter()


@router.post("/research/{research_id}/apply/", response_model=schemas.ResearchBase)
def apply_for_research(
        research_id: UUID,
        description: str,
        current_user: User = Depends(auth.require_user),
        db: Session = Depends(get_db)
):
    """
    Allows a user to apply for a research by appending their user_id to the application column.
    """
    user_id=current_user.user_id
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.professor:
        raise HTTPException(status_code=403, detail="Permission denied,Not a student")
    student_id = db_user.id
    db_research = crud.apply_for_research(db=db, research_id=research_id, student_id=student_id,
                                          description=description)
    if db_research is None:
        raise HTTPException(status_code=404, detail="Research not found")
    return db_research


# accept application
@router.post("/research/{research_id}/accept/", response_model=schemas.ResearchBase)
def accept_application(
        research_id: UUID,
        current_user: User = Depends(auth.require_user),
        db: Session = Depends(get_db)
):
    user_id = current_user.user_id
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
        current_user: User = Depends(auth.require_user),
        db: Session = Depends(get_db)
):
    user_id = current_user.user_id
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
    page: int = Query(1, ge=1, alias="page"),  # 确保页码不小于1
    page_size: int = Query(10, ge=1, alias="page_size"),  # 确保每页大小不小于1
    db: Session = Depends(get_db),
):
    # 计算跳过的记录数
    skip = (page - 1) * page_size
    # 查询数据库获取分页数据，按 created_at 字段倒序排列
    applications = crud.get_applications(db, skip=skip, limit=page_size)
    return applications

