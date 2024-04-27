# schemas.py
from pydantic import BaseModel, UUID4, Field
from typing import Optional

class UserUpdate(BaseModel):
    name: Optional[str] = None
    professor: Optional[bool] = None

class UserCreate(BaseModel):
    name: str
    professor: bool


class User:
    id: UUID4
    name: str
    professor: bool
    class Config:
        orm_mode = True