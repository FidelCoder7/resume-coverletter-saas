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
    metadata = metadata
