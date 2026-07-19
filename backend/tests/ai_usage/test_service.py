from decimal import Decimal
from unittest.mock import MagicMock
from uuid import uuid4

from app.ai.contracts import AIExecutionMetadata
from app.ai_usage.models import AIUsage
from app.ai_usage.service import AIUsageService
from app.common.constants import (
    AIFeature,
    AIRequestStatus,
)


def build_metadata() -> AIExecutionMetadata:
    return AIExecutionMetadata(
        provider="openai",
        model="gpt-4.1-mini",
        prompt_version="v1",
        prompt_tokens=120,
        completion_tokens=80,
        total_tokens=200,
        latency_ms=450,
    )


def build_usage() -> AIUsage:
    return AIUsage(
        user_id=uuid4(),
        resume_id=None,
        cover_letter_id=None,
        feature=AIFeature.RESUME_GENERATION,
        provider="openai",
        model="gpt-4.1-mini",
        prompt_version="v1",
        prompt_tokens=120,
        completion_tokens=80,
        total_tokens=200,
        estimated_cost=Decimal("0.020000"),
        latency_ms=450,
        status=AIRequestStatus.SUCCESS,
        error_message=None,
    )


def build_service():
    repository = MagicMock()

    service = AIUsageService(
        repository=repository,
    )

    return service, repository


def test_record_success_creates_usage():
    service, repository = build_service()

    usage = build_usage()

    repository.create.return_value = usage

    result = service.record_success(
        user_id=uuid4(),
        feature=AIFeature.RESUME_GENERATION,
        metadata=build_metadata(),
    )

    repository.create.assert_called_once()

    created_usage = repository.create.call_args.args[0]

    assert created_usage.provider == "openai"
    assert created_usage.model == "gpt-4.1-mini"
    assert created_usage.prompt_version == "v1"
    assert created_usage.prompt_tokens == 120
    assert created_usage.completion_tokens == 80
    assert created_usage.total_tokens == 200
    assert created_usage.latency_ms == 450
    assert created_usage.status is AIRequestStatus.SUCCESS
    assert created_usage.error_message is None

    assert result is usage


def test_record_failure_creates_usage():
    service, repository = build_service()

    usage = build_usage()
    usage.status = AIRequestStatus.FAILED

    repository.create.return_value = usage

    result = service.record_failure(
        user_id=uuid4(),
        feature=AIFeature.COVER_LETTER_GENERATION,
        metadata=build_metadata(),
        error_message="Provider timeout",
    )

    repository.create.assert_called_once()

    created_usage = repository.create.call_args.args[0]

    assert created_usage.feature is AIFeature.COVER_LETTER_GENERATION
    assert created_usage.status is AIRequestStatus.FAILED
    assert created_usage.error_message == "Provider timeout"

    assert result is usage


def test_get_usage_delegates_to_repository():
    service, repository = build_service()

    usage = build_usage()

    repository.get_by_id.return_value = usage

    usage_id = uuid4()

    result = service.get_usage(
        usage_id=usage_id,
    )

    repository.get_by_id.assert_called_once_with(
        usage_id,
    )

    assert result is usage


def test_list_user_history_delegates_to_repository():
    service, repository = build_service()

    usage = build_usage()

    repository.list_by_user.return_value = [
        usage,
    ]

    user_id = uuid4()

    result = service.list_user_history(
        user_id=user_id,
    )

    repository.list_by_user.assert_called_once_with(
        user_id,
    )

    assert result == [usage]


def test_list_resume_history_delegates_to_repository():
    service, repository = build_service()

    usage = build_usage()

    repository.list_by_resume.return_value = [
        usage,
    ]

    resume_id = uuid4()

    result = service.list_resume_history(
        resume_id=resume_id,
    )

    repository.list_by_resume.assert_called_once_with(
        resume_id,
    )

    assert result == [usage]


def test_list_cover_letter_history_delegates_to_repository():
    service, repository = build_service()

    usage = build_usage()

    repository.list_by_cover_letter.return_value = [
        usage,
    ]

    cover_letter_id = uuid4()

    result = service.list_cover_letter_history(
        cover_letter_id=cover_letter_id,
    )

    repository.list_by_cover_letter.assert_called_once_with(
        cover_letter_id,
    )

    assert result == [usage]
