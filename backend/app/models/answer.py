from typing import List, Optional, TYPE_CHECKING
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, ForeignKey, Integer, CheckConstraint
from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models import Chain, Question, Configuration, AnswerComment


class Answer(BaseModel):
    """SQLAlchemy model for generated answers"""

    __tablename__ = "answers"

    chain_id: Mapped[UUID] = mapped_column(
        ForeignKey("chains.id", ondelete="CASCADE"), nullable=False
    )
    question_id: Mapped[UUID] = mapped_column(
        ForeignKey("questions.id", ondelete="CASCADE"), nullable=False
    )
    configuration_id: Mapped[UUID] = mapped_column(
        ForeignKey("configurations.id", ondelete="CASCADE"), nullable=False
    )
    generated_answer: Mapped[str] = mapped_column(Text, nullable=False)
    score: Mapped[Optional[int]] = mapped_column(Integer)

    # Constraints
    __table_args__ = (
        CheckConstraint("score >= 0 AND score <= 5", name="valid_score_range"),
    )

    # Relationships
    chain: Mapped["Chain"] = relationship(back_populates="answers")
    question: Mapped["Question"] = relationship(back_populates="answers")
    configuration: Mapped["Configuration"] = relationship(
        back_populates="answers"
    )
    comments: Mapped[List["AnswerComment"]] = relationship(
        back_populates="answer", cascade="all, delete-orphan", lazy="selectin"
    )
