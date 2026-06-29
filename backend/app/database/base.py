from sqlalchemy.orm import DeclarativeBase

from app.database.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class Base(
    DeclarativeBase,
    UUIDPrimaryKeyMixin,
    TimestampMixin,
):
    """Base class for all ORM models."""
