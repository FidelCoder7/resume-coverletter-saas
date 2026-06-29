"""
Import every ORM model here.

Alembic imports this module to discover
all SQLAlchemy metadata.
"""

from app.database.base import Base
from app.users.models import User

# Future imports
# from app.users.models import User
# from app.resumes.models import Resume

__all__ = [
    "Base",
    "User",
]
