from typing import List, Optional, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, String, Text
from datetime import datetime
from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models import Chain, Question


class Session(BaseModel):
    """SQLAlchemy model for evaluation sessions"""

    __tablename__ = "sessions"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    last_modified: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False,
        sort_order=-1,
    )

    # Relationships
    chains: Mapped[List["Chain"]] = relationship(
        back_populates="session", cascade="all, delete-orphan", lazy="selectin"
    )
    questions: Mapped[List["Question"]] = relationship(
        back_populates="session", cascade="all, delete-orphan", lazy="selectin"
    )
