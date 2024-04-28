import datetime
import uuid
from typing import Optional

from sqlalchemy import Boolean, DateTime, Integer, PrimaryKeyConstraint, Text, Uuid, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Application(Base):
    __tablename__ = 'application'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='application_pkey'),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    research_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    student_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    status: Mapped[Optional[int]] = mapped_column(Integer)
    letter: Mapped[Optional[str]] = mapped_column(Text)
    time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('now()'))


class Research(Base):
    __tablename__ = 'research'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='research_pkey'),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    title: Mapped[Optional[str]] = mapped_column(Text)
    professor_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    description: Mapped[Optional[str]] = mapped_column(Text)
    money: Mapped[Optional[int]] = mapped_column(Integer)
    location: Mapped[Optional[str]] = mapped_column(Text)
    univercity: Mapped[Optional[str]] = mapped_column(Text)
    isfulltime: Mapped[Optional[bool]] = mapped_column(Boolean)
    time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('now()'))


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='users_pkey'),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    name: Mapped[Optional[str]] = mapped_column(Text)
    professor: Mapped[Optional[bool]] = mapped_column(Boolean)
    lastname: Mapped[Optional[str]] = mapped_column(Text)
    firstname: Mapped[Optional[str]] = mapped_column(Text)
    gender: Mapped[Optional[str]] = mapped_column(Text)
    pronounce: Mapped[Optional[str]] = mapped_column(Text)
    biography: Mapped[Optional[str]] = mapped_column(Text)
    eduemail: Mapped[Optional[str]] = mapped_column(Text)
    phonenumber: Mapped[Optional[int]] = mapped_column(Integer)
    personal_homepage: Mapped[Optional[str]] = mapped_column(Text)
    featured_publications: Mapped[Optional[str]] = mapped_column(Text)
    award_honor: Mapped[Optional[str]] = mapped_column(Text)
    department: Mapped[Optional[str]] = mapped_column(Text)
    photo: Mapped[Optional[str]] = mapped_column(Text)
    research_area: Mapped[Optional[int]] = mapped_column(Integer)
    middlename: Mapped[Optional[str]] = mapped_column(Text)
    university: Mapped[Optional[str]] = mapped_column(Text)
    time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('now()'))
    user_id: Mapped[Optional[str]] = mapped_column(Text)
