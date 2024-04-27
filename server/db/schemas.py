# schemas.py
from pydantic import BaseModel, UUID4, Field
from typing import Optional

class UserUpdate(BaseModel):
    name: Optional[str] = None
    professor: Optional[bool] = None

class UserCreate(BaseModel):
    name: str
    professor: bool


