from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime as dt

Base = declarative_base()


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=dt.now)
    questions = relationship(
        "Question",
        back_populates="session",
        lazy="selectin",
        cascade="all, delete-orphan",
    )


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    content = Column(String)
    created_at = Column(DateTime, default=dt.now)

    session = relationship(
        "Session", back_populates="questions", lazy="selectin"
    )
    answers = relationship(
        "Answer",
        back_populates="question",
        lazy="selectin",
        cascade="all, delete-orphan",
    )


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    content = Column(String)
    created_at = Column(DateTime, default=dt.now)

    question = relationship(
        "Question", lazy="selectin", back_populates="answers"
    )
