from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .database import Base


class User(Base):
    __tablename__ = 'User'  # Assuming the actual table name is 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text)
    professor = Column(Boolean)
    lastname = Column(Text)
    firstname = Column(Text)
    gender = Column(Text)
    pronounce = Column(Text)
    biography = Column(Text)
    eduemail = Column(Text)
    phonenumber = Column(Integer)
    personal_homepage = Column(Text)
    featured_publications = Column(Text)
    award_honor = Column(Text)
    department = Column(Text)
    photo = Column(Text)
    research_area = Column(Integer)
    middlename = Column(Text)
    university = Column(Text)
    time = Column(DateTime(True), server_default=text("now()"))


class Research(Base):
    __tablename__ = 'research'
    id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(Text, index=True)
    professor_id = Column(UUID(as_uuid=True))
    description = Column(Text)
    money = Column(Integer)
    location = Column(Text)
    univercity = Column(Text)
    isfulltime = Column(Boolean)
    time = Column(DateTime(True), server_default=text("now()"))



class Application(Base):
    __tablename__ = 'application'
    id = Column(UUID(as_uuid=True), primary_key=True)
    research_id = Column(UUID(as_uuid=True))
    student_id = Column(UUID(as_uuid=True))
    status = Column(Integer)
    letter= Column(Text)
    time = Column(DateTime(True), server_default=text("now()"))



