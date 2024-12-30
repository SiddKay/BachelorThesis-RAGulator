from typing import List, TYPE_CHECKING
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models import Session, Answer, Configuration


class Chain(BaseModel):
    """SQLAlchemy model for LCEL chains"""

    __tablename__ = "chains"

    session_id: Mapped[UUID] = mapped_column(
        ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False
    )
    file_name: Mapped[str] = mapped_column(String(512), nullable=False)

    # Relationships
    session: Mapped["Session"] = relationship(back_populates="chains")
    answers: Mapped[List["Answer"]] = relationship(
        back_populates="chain", cascade="all, delete-orphan", lazy="selectin"
    )
    configurations: Mapped[List["Configuration"]] = relationship(
        back_populates="chain", cascade="all, delete-orphan", lazy="selectin"
    )
