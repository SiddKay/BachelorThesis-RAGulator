from typing import TYPE_CHECKING
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, Text, ForeignKey
from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models import Answer


class AnswerComment(BaseModel):
    """SQLAlchemy model for answer comments"""

    __tablename__ = "answer_comments"

    answer_id: Mapped[UUID] = mapped_column(
        ForeignKey("answers.id", ondelete="CASCADE"), nullable=False
    )
    comment_text: Mapped[str] = mapped_column(Text, nullable=False)
    last_modified: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False,
        sort_order=-1,
    )

    # Relationships
    answer: Mapped["Answer"] = relationship(back_populates="comments")
