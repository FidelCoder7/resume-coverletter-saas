from collections.abc import Iterator

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

engine: Engine = create_engine(
    settings.database_url,
    echo=settings.app_env == "development",
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
