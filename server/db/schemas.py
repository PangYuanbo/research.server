from pydantic import BaseModel, UUID4, Field, EmailStr
from typing import Optional


# Shared properties
class UserBase(BaseModel):
    name: Optional[str] = None
    professor: Optional[bool] = None
    lastname: Optional[str] = None
    firstname: Optional[str] = None
    gender: Optional[str] = None
    pronounce: Optional[str] = None
    biography: Optional[str] = None
    eduemail: Optional[EmailStr] = None
    phonenumber: Optional[int] = None
    personal_homepage: Optional[str] = None
    featured_publications: Optional[str] = None
    award_honor: Optional[str] = None
    department: Optional[str] = None
    photo: Optional[str] = None
    research_area: Optional[int] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    name: str
    professor: bool


# Properties to receive via API on update
class UserUpdate(UserBase):
    pass


# Properties to return to client
class User(UserBase):
    id: UUID4

    class Config:
        orm_mode = True
