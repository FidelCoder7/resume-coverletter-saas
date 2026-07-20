from unittest.mock import MagicMock, patch

from app.ai.dependencies import (
    get_ai_provider,
    get_ai_service,
)
from app.ai.openai_provider import OpenAIProvider
from app.ai.retry import RetryService
from app.ai.service import AIService


@patch.object(OpenAIProvider, "__init__", return_value=None)
def test_get_ai_provider_returns_openai_provider(_):
    provider = get_ai_provider()

    assert isinstance(
        provider,
        OpenAIProvider,
    )


@patch("app.ai.dependencies.get_retry_service")
@patch.object(OpenAIProvider, "__init__", return_value=None)
def test_get_ai_service_returns_ai_service(
    _,
    mock_get_retry_service,
):
    mock_get_retry_service.return_value = MagicMock(
        spec=RetryService,
    )

    service = get_ai_service()

    assert isinstance(
        service,
        AIService,
    )


@patch("app.ai.dependencies.get_retry_service")
@patch.object(OpenAIProvider, "__init__", return_value=None)
def test_ai_service_uses_openai_provider(
    _,
    mock_get_retry_service,
):
    mock_get_retry_service.return_value = MagicMock(
        spec=RetryService,
    )

    service = get_ai_service()

    assert isinstance(
        service.provider,
        OpenAIProvider,
    )


@patch("app.ai.dependencies.get_retry_service")
@patch.object(OpenAIProvider, "__init__", return_value=None)
def test_ai_service_has_retry_service(
    _,
    mock_get_retry_service,
):
    retry_service = MagicMock(
        spec=RetryService,
    )

    mock_get_retry_service.return_value = retry_service

    service = get_ai_service()

    assert service.retry_service is retry_service
