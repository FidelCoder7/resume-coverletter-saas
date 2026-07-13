import os
from collections.abc import Generator

# Must be set BEFORE importing the application.
os.environ["ENV_FILE"] = ".env.test"

import pytest
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Session, sessionmaker

from alembic import command
from app.ai.dependencies import get_ai_service
from app.ai.providers import AIProvider
from app.ai.schemas import (
    CoverLetterGenerationRequest,
    CoverLetterGenerationResponse,
)
from app.ai.service import AIService
from app.core.config import settings
from app.core.rate_limit import limiter
from app.database.session import get_db
from app.mail.service import MailService
from app.main import app

engine = create_engine(
    settings.DATABASE_URL,
    future=True,
)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


class FakeAIProvider(AIProvider):
    """
    Fake AI provider used during tests.
    """

    def generate_cover_letter(
        self,
        request: CoverLetterGenerationRequest,
    ) -> CoverLetterGenerationResponse:
        return CoverLetterGenerationResponse(
            content=("This is a generated cover letter for testing purposes."),
        )


@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    """
    Apply all Alembic migrations once before the test session.
    """

    alembic_cfg = Config("alembic.ini")

    alembic_cfg.set_main_option(
        "sqlalchemy.url",
        settings.DATABASE_URL,
    )

    command.upgrade(
        alembic_cfg,
        "head",
    )

    yield


@pytest.fixture(scope="session")
def db_engine():
    yield engine
    engine.dispose()


@pytest.fixture()
def connection(
    db_engine,
    apply_migrations,
) -> Generator[Connection]:
    """
    One database connection per test.
    """

    connection = db_engine.connect()
    transaction = connection.begin()

    try:
        yield connection
    finally:
        transaction.rollback()
        connection.close()


@pytest.fixture()
def db_session(
    connection: Connection,
) -> Generator[Session]:
    """
    SQLAlchemy session using nested SAVEPOINT transactions.

    Application code may freely call session.commit()
    without leaking data between tests.
    """

    session = TestingSessionLocal(
        bind=connection,
    )

    session.begin_nested()

    @event.listens_for(
        session,
        "after_transaction_end",
    )
    def restart_savepoint(
        session_,
        transaction,
    ):
        if transaction.nested and not transaction._parent.nested:
            session_.begin_nested()

    try:
        yield session

    finally:
        event.remove(
            session,
            "after_transaction_end",
            restart_savepoint,
        )

        session.close()


@pytest.fixture()
def fake_ai_service() -> AIService:
    """
    AI service backed by a deterministic fake provider.
    """

    return AIService(
        provider=FakeAIProvider(),
    )


@pytest.fixture()
def client(
    db_session: Session,
    fake_ai_service: AIService,
) -> Generator[TestClient]:
    """
    FastAPI TestClient using the testing database.
    """

    def override_get_db():
        yield db_session

    def override_get_ai_service():
        return fake_ai_service

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_ai_service] = override_get_ai_service

    limiter.enabled = False

    with TestClient(app) as client:
        yield client

    limiter.enabled = True
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def disable_email(monkeypatch):
    """
    Prevent real emails from being sent during tests.
    """

    def fake_send(self, *args, **kwargs):
        return None

    monkeypatch.setattr(
        MailService,
        "send",
        fake_send,
    )
