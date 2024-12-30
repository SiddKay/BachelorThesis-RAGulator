from typing import List, Any, Dict, TYPE_CHECKING
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models import Session, Answer, Chain


class Configuration(BaseModel):
    """SQLAlchemy model for chain configurations"""

    __tablename__ = "configurations"

    session_id: Mapped[UUID] = mapped_column(
        ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False
    )
    chain_id: Mapped[UUID] = mapped_column(
        ForeignKey("chains.id", ondelete="CASCADE"), nullable=False
    )
    config_schema: Mapped[Dict[str, Any]] = mapped_column(
        JSONB,
        nullable=True,
        comment="JSON schema defining valid configuration options",
    )
    config_values: Mapped[Dict[str, Any]] = mapped_column(
        JSONB, nullable=True, comment="Current configuration values"
    )

    # Relationships
    chain: Mapped["Chain"] = relationship(back_populates="configurations")
    answers: Mapped[List["Answer"]] = relationship(
        back_populates="configuration",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
