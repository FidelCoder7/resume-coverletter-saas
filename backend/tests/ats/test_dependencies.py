from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from app.ai.service import AIService
from app.ats.ai_service import ATSAIService
from app.ats.dependencies import (
    get_ats_ai_service,
    get_ats_service,
)
from app.ats.service import ATSService


def test_get_ats_ai_service_builds_service():
    db = MagicMock(spec=Session)
    ai_service = MagicMock(spec=AIService)

    service = get_ats_ai_service(
        db=db,
        ai_service=ai_service,
    )

    assert isinstance(
        service,
        ATSAIService,
    )

    assert service.ai_service is ai_service
    assert service.ai_usage_service.repository.db is db


def test_get_ats_service_builds_service():
    db = MagicMock(spec=Session)

    ats_ai_service = MagicMock(
        spec=ATSAIService,
    )

    service = get_ats_service(
        db=db,
        ai_service=ats_ai_service,
    )

    assert isinstance(
        service,
        ATSService,
    )

    assert service.repository.db is db
    assert service.ai_service is ats_ai_service
