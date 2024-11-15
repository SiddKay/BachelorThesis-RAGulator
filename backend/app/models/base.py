from datetime import datetime
from sqlalchemy import DateTime
from uuid import UUID as PyUUID, uuid4
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


# Base SQLAlchemy Model
class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models"""

    pass


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[PyUUID] = mapped_column(
        PgUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True,
        sort_order=-3,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False,
        sort_order=-2,
    )
