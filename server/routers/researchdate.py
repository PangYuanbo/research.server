from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from ..db import schemas, crud, database, model
from ..db.dependencies import get_db


router = APIRouter()


@router.post("/research/", response_model=schemas.ResearchBase)
def create_research_entry(
        research: schemas.ResearchCreate,
        db: Session = Depends(get_db)
):
    return crud.create_research(db=db, research_create=research)


@router.get("/research/{research_id}", response_model=schemas.ResearchBase)
def read_research(research_id: UUID, db: Session = Depends(get_db)):
    db_research = crud.get_research(db, research_id=research_id)
    if db_research is None:
        raise HTTPException(status_code=404, detail="Research not found")
    return db_research


@router.get("/researches/", response_model=List[schemas.ResearchBase])
def read_researches(
    page: int = Query(1, ge=1, alias="page"),  # 确保页码大于等于1
    page_size: int = Query(10, ge=1, le=100, alias="page_size"),  # 确保每页大小在1到100之间
    db: Session = Depends(get_db)
):
    skip = (page - 1) * page_size
    researches = crud.get_researches(db, skip=skip, limit=page_size)
    return researches


# Return all the research projects of this professor in the research table based on the professor id of the post,
# and display them in a paged fashion.
@router.post("/researches/professor/", response_model=List[schemas.ResearchBase])
def read_researches_by_professor(
    user_id: UUID,
    page: int = Query(1, ge=1, alias="page"),  # 确保页码大于等于1
    page_size: int = Query(10, ge=1, le=100, alias="page_size"),  # 确保每页大小在1到100之间
    db: Session = Depends(get_db)
):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.professor:
        professor_id = user_id
        skip = (page - 1) * page_size
        researches = crud.get_researches_by_professor(db, professor_id=professor_id, skip=skip, limit=page_size)
        if researches is None:
            raise HTTPException(status_code=404, detail="Research not found")
        return researches
    else:
        raise HTTPException(status_code=403, detail="Permission denied,Not a professor")
