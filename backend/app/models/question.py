from typing import List, Optional, TYPE_CHECKING
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, Text, ForeignKey
from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models import Session, Answer


class Question(BaseModel):
    """SQLAlchemy model for evaluation questions"""

    __tablename__ = "questions"

    session_id: Mapped[UUID] = mapped_column(
        ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False
    )
    question_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        info={"description": "The actual question content"},
    )
    expected_answer: Mapped[Optional[str]] = mapped_column(
        Text, info={"description": "Reference answer for evaluation"}
    )
    last_modified: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False,
        sort_order=-1,
    )

    # Relationships
    session: Mapped["Session"] = relationship(back_populates="questions")
    answers: Mapped[List["Answer"]] = relationship(
        back_populates="question",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
