from unittest.mock import patch

from app.ai.dependencies import (
    get_ai_provider,
    get_ai_service,
)
from app.ai.openai_provider import OpenAIProvider
from app.ai.service import AIService


@patch.object(OpenAIProvider, "__init__", return_value=None)
def test_get_ai_provider_returns_openai_provider(_):
    provider = get_ai_provider()

    assert isinstance(
        provider,
        OpenAIProvider,
    )


@patch.object(OpenAIProvider, "__init__", return_value=None)
def test_get_ai_service_returns_ai_service(_):
    service = get_ai_service()

    assert isinstance(
        service,
        AIService,
    )


@patch.object(OpenAIProvider, "__init__", return_value=None)
def test_ai_service_uses_openai_provider(_):
    service = get_ai_service()

    assert isinstance(
        service.provider,
        OpenAIProvider,
    )
