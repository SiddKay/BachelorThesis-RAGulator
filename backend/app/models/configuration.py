from typing import List, Any, Dict, Optional, TYPE_CHECKING
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models import Session, Answer


class Configuration(BaseModel):
    """SQLAlchemy model for chain configurations"""

    __tablename__ = "configurations"

    session_id: Mapped[UUID] = mapped_column(
        ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False
    )
    prompt_template: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSONB, nullable=True
    )
    llm_parameters: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSONB, nullable=True
    )

    # Relationships
    session: Mapped["Session"] = relationship(back_populates="configurations")
    answers: Mapped[List["Answer"]] = relationship(
        back_populates="configuration",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
