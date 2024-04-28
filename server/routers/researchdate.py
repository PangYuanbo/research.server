from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from server.db import schemas, crud, database, model

from server.db import schemas
from server.db.dependencies import get_db
from fastapi import FastAPI

router = APIRouter()


@router.post("/research/", response_model=schemas.ResearchInDB)
def create_research_entry(
        research: schemas.ResearchCreate,
        professor_id: UUID,
        db: Session = Depends(get_db)
):
    return crud.create_research(db=db, research_create=research, professor_id=professor_id)


@router.get("/research/{research_id}", response_model=schemas.ResearchBase)
def read_research(research_id: UUID, db: Session = Depends(get_db)):
    db_research = crud.get_research(db, research_id=research_id)
    if db_research is None:
        raise HTTPException(status_code=404, detail="Research not found")
    return db_research


@router.get("/researches/", response_model=List[schemas.ResearchBase])
def read_researches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    researches = crud.get_researches(db, skip=skip, limit=limit)
    return researches


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
    db_research = crud.apply_for_research(db=db, research_id=research_id, student_id=student_id, description=description)
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


