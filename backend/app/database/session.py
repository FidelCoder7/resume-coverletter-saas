from collections.abc import Iterator

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.common.constants import Environment
from app.core.config import settings

engine: Engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.APP_ENV == Environment.DEVELOPMENT,
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def get_db() -> Iterator[Session]:
    """
    FastAPI dependency that yields a database session.
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
