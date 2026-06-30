from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from app.database.metadata import metadata
from app.database.mixins import (
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)


class Base(
    DeclarativeBase,
    UUIDPrimaryKeyMixin,
    TimestampMixin,
):
    """
    Base class for every ORM model.
    """

    metadata: MetaData = metadata

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.id})>"
