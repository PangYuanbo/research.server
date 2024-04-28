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
