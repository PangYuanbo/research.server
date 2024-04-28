from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from server.db.model import Research
from server.db import schemas, crud, database, model
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
def read_researches(
    page: int = Query(1, ge=1, alias="page"),  # 确保页码大于等于1
    page_size: int = Query(10, ge=1, le=100, alias="page_size"),  # 确保每页大小在1到100之间
    db: Session = Depends(get_db)
):
    skip = (page - 1) * page_size
    researches = crud.get_researches(db, skip=skip, limit=page_size)
    return researches


