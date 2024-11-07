from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict
from uuid import UUID, uuid4
from sqlalchemy import (
    Text,
    String,
    TIMESTAMP,
    func,
    Enum as SQLAEnum,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID as SQLUUID, JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# Base SQLAlchemy Model
class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models"""

    pass


# Enums
class ScoreRange(str, Enum):
    """Enum for answer scores"""

    SCORE_0 = "0"
    SCORE_1 = "1"
    SCORE_2 = "2"
    SCORE_3 = "3"
    SCORE_4 = "4"
    SCORE_5 = "5"


# SQLAlchemy Models
class Session(Base):
    """SQLAlchemy model for evaluation sessions"""

    __tablename__ = "sessions"

    id: Mapped[UUID] = mapped_column(SQLUUID, primary_key=True, default=uuid4)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=func.now(),
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    last_accessed: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
    )

    # Relationships
    chain_evaluations: Mapped[List["ChainEvaluation"]] = relationship(
        back_populates="session", cascade="all, delete-orphan"
    )
    questions: Mapped[List["Question"]] = relationship(
        back_populates="session", cascade="all, delete-orphan"
    )


class Chain(Base):
    """SQLAlchemy model for LangChain expression chains"""

    __tablename__ = "chains"

    id: Mapped[UUID] = mapped_column(SQLUUID, primary_key=True, default=uuid4)
    file_name: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True
    )
    file_path: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    imported_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=func.now(),
    )

    # Relationships
    evaluations: Mapped[List["ChainEvaluation"]] = relationship(
        back_populates="chain", cascade="all, delete-orphan"
    )


class Question(Base):
    """SQLAlchemy model for evaluation questions"""

    __tablename__ = "questions"

    id: Mapped[UUID] = mapped_column(SQLUUID, primary_key=True, default=uuid4)
    session_id: Mapped[UUID] = mapped_column(
        SQLUUID, ForeignKey("sessions.id", ondelete="CASCADE")
    )
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    expected_answer: Mapped[Optional[str]] = mapped_column(Text)
    sequence_number: Mapped[int] = mapped_column(nullable=False)

    # Relationships
    session: Mapped["Session"] = relationship(back_populates="questions")
    answers: Mapped[List["Answer"]] = relationship(
        back_populates="question", cascade="all, delete-orphan"
    )

    # Constraints
    __table_args__ = (
        UniqueConstraint(
            "session_id",
            "sequence_number",
            name="questions_sequence_session_unique",
        ),
    )


class Configuration(Base):
    """SQLAlchemy model for chain configurations"""

    __tablename__ = "configurations"

    id: Mapped[UUID] = mapped_column(SQLUUID, primary_key=True, default=uuid4)
    prompt_template: Mapped[Optional[Dict]] = mapped_column(JSONB)
    model_params: Mapped[Optional[Dict]] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=func.now(),
    )

    # Relationships
    answers: Mapped[List["Answer"]] = relationship(
        back_populates="configuration"
    )


class ChainEvaluation(Base):
    """SQLAlchemy model for chain evaluation runs"""

    __tablename__ = "chain_evaluations"

    id: Mapped[UUID] = mapped_column(SQLUUID, primary_key=True, default=uuid4)
    session_id: Mapped[UUID] = mapped_column(
        SQLUUID, ForeignKey("sessions.id", ondelete="CASCADE")
    )
    chain_id: Mapped[UUID] = mapped_column(
        SQLUUID, ForeignKey("chains.id", ondelete="CASCADE")
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=func.now(),
    )

    # Relationships
    session: Mapped["Session"] = relationship(
        back_populates="chain_evaluations"
    )
    chain: Mapped["Chain"] = relationship(back_populates="evaluations")
    answers: Mapped[List["Answer"]] = relationship(
        back_populates="evaluation", cascade="all, delete-orphan"
    )


class Answer(Base):
    """SQLAlchemy model for generated answers"""

    __tablename__ = "answers"

    id: Mapped[UUID] = mapped_column(SQLUUID, primary_key=True, default=uuid4)
    evaluation_id: Mapped[UUID] = mapped_column(
        SQLUUID, ForeignKey("chain_evaluations.id", ondelete="CASCADE")
    )
    question_id: Mapped[UUID] = mapped_column(
        SQLUUID, ForeignKey("questions.id", ondelete="CASCADE")
    )
    config_id: Mapped[UUID] = mapped_column(
        SQLUUID, ForeignKey("configurations.id", ondelete="CASCADE")
    )
    generated_text: Mapped[str] = mapped_column(Text, nullable=False)
    score: Mapped[Optional[ScoreRange]] = mapped_column(SQLAEnum(ScoreRange))
    generated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=func.now(),
    )

    # Relationships
    evaluation: Mapped["ChainEvaluation"] = relationship(
        back_populates="answers"
    )
    question: Mapped["Question"] = relationship(back_populates="answers")
    configuration: Mapped["Configuration"] = relationship(
        back_populates="answers"
    )
    comments: Mapped[List["AnswerComment"]] = relationship(
        back_populates="answer", cascade="all, delete-orphan"
    )


class AnswerComment(Base):
    """SQLAlchemy model for answer comments"""

    __tablename__ = "answer_comments"

    id: Mapped[UUID] = mapped_column(SQLUUID, primary_key=True, default=uuid4)
    answer_id: Mapped[UUID] = mapped_column(
        SQLUUID, ForeignKey("answers.id", ondelete="CASCADE")
    )
    comment_text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=func.now(),
    )

    # Relationships
    answer: Mapped["Answer"] = relationship(back_populates="comments")
