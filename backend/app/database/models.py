"""
Import every ORM model here.

Alembic uses this file to discover metadata.
"""

from app.database.base import Base

__all__ = ["Base"]
