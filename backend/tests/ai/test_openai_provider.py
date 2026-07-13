from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest
from openai import APITimeoutError, OpenAIError, RateLimitError

from app.ai.exceptions import (
    AIConfigurationError,
    AIGenerationError,
    AIProviderError,
    AIRateLimitError,
    AITimeoutError,
)
from app.ai.openai_provider import OpenAIProvider
from app.ai.schemas import CoverLetterGenerationRequest


def build_request() -> CoverLetterGenerationRequest:
    return CoverLetterGenerationRequest(
        company_name="OpenAI",
        job_title="Backend Engineer",
        job_description="Build scalable backend APIs.",
        resume_content="Experienced Python developer.",
    )


def build_response(
    *,
    content: str = "Generated cover letter.",
    finish_reason: str = "stop",
):
    return SimpleNamespace(
        choices=[
            SimpleNamespace(
                finish_reason=finish_reason,
                message=SimpleNamespace(
                    content=content,
                ),
            ),
        ],
        usage=SimpleNamespace(
            prompt_tokens=120,
            completion_tokens=180,
            total_tokens=300,
        ),
    )


@patch("app.ai.openai_provider.settings")
@patch("app.ai.openai_provider.OpenAI")
def test_generate_cover_letter_success(
    mock_openai,
    mock_settings,
):
    mock_settings.OPENAI_API_KEY = "test-key"
    mock_settings.OPENAI_MODEL = "gpt-5"
    mock_settings.OPENAI_TIMEOUT = 60
    mock_settings.OPENAI_MAX_TOKENS = 1200
    mock_settings.OPENAI_TEMPERATURE = 0.7

    client = MagicMock()
    client.chat.completions.create.return_value = build_response()

    mock_openai.return_value = client

    provider = OpenAIProvider()

    response = provider.generate_cover_letter(
        build_request(),
    )

    assert response.content == "Generated cover letter."

    assert response.metadata.provider == "openai"
    assert response.metadata.model == "gpt-5"
    assert response.metadata.prompt_version == "cover_letter_v1"

    assert response.metadata.prompt_tokens == 120
    assert response.metadata.completion_tokens == 180
    assert response.metadata.total_tokens == 300

    assert response.metadata.latency_ms is not None
    assert response.metadata.latency_ms >= 0


@patch("app.ai.openai_provider.settings")
def test_missing_api_key_raises_configuration_error(
    mock_settings,
):
    mock_settings.OPENAI_API_KEY = None

    with pytest.raises(
        AIConfigurationError,
    ):
        OpenAIProvider()


@patch("app.ai.openai_provider.settings")
@patch("app.ai.openai_provider.OpenAI")
def test_empty_choices_raise_generation_error(
    mock_openai,
    mock_settings,
):
    mock_settings.OPENAI_API_KEY = "key"
    mock_settings.OPENAI_MODEL = "gpt-5"
    mock_settings.OPENAI_TIMEOUT = 60
    mock_settings.OPENAI_MAX_TOKENS = 1200
    mock_settings.OPENAI_TEMPERATURE = 0.7

    client = MagicMock()

    client.chat.completions.create.return_value = SimpleNamespace(
        choices=[],
    )

    mock_openai.return_value = client

    provider = OpenAIProvider()

    with pytest.raises(
        AIGenerationError,
    ):
        provider.generate_cover_letter(
            build_request(),
        )


@patch("app.ai.openai_provider.settings")
@patch("app.ai.openai_provider.OpenAI")
def test_empty_content_raises_generation_error(
    mock_openai,
    mock_settings,
):
    mock_settings.OPENAI_API_KEY = "key"
    mock_settings.OPENAI_MODEL = "gpt-5"
    mock_settings.OPENAI_TIMEOUT = 60
    mock_settings.OPENAI_MAX_TOKENS = 1200
    mock_settings.OPENAI_TEMPERATURE = 0.7

    client = MagicMock()

    client.chat.completions.create.return_value = build_response(
        content="",
    )

    mock_openai.return_value = client

    provider = OpenAIProvider()

    with pytest.raises(
        AIGenerationError,
    ):
        provider.generate_cover_letter(
            build_request(),
        )


@patch("app.ai.openai_provider.settings")
@patch("app.ai.openai_provider.OpenAI")
def test_truncated_response_raises_generation_error(
    mock_openai,
    mock_settings,
):
    mock_settings.OPENAI_API_KEY = "key"
    mock_settings.OPENAI_MODEL = "gpt-5"
    mock_settings.OPENAI_TIMEOUT = 60
    mock_settings.OPENAI_MAX_TOKENS = 1200
    mock_settings.OPENAI_TEMPERATURE = 0.7

    client = MagicMock()

    client.chat.completions.create.return_value = build_response(
        finish_reason="length",
    )

    mock_openai.return_value = client

    provider = OpenAIProvider()

    with pytest.raises(
        AIGenerationError,
    ):
        provider.generate_cover_letter(
            build_request(),
        )


@patch("app.ai.openai_provider.settings")
@patch("app.ai.openai_provider.OpenAI")
def test_timeout_translated(
    mock_openai,
    mock_settings,
):
    mock_settings.OPENAI_API_KEY = "key"
    mock_settings.OPENAI_MODEL = "gpt-5"
    mock_settings.OPENAI_TIMEOUT = 60
    mock_settings.OPENAI_MAX_TOKENS = 1200
    mock_settings.OPENAI_TEMPERATURE = 0.7

    client = MagicMock()

    client.chat.completions.create.side_effect = APITimeoutError(
        request=MagicMock(),
    )

    mock_openai.return_value = client

    provider = OpenAIProvider()

    with pytest.raises(
        AITimeoutError,
    ):
        provider.generate_cover_letter(
            build_request(),
        )


@patch("app.ai.openai_provider.settings")
@patch("app.ai.openai_provider.OpenAI")
def test_rate_limit_translated(
    mock_openai,
    mock_settings,
):
    mock_settings.OPENAI_API_KEY = "key"
    mock_settings.OPENAI_MODEL = "gpt-5"
    mock_settings.OPENAI_TIMEOUT = 60
    mock_settings.OPENAI_MAX_TOKENS = 1200
    mock_settings.OPENAI_TEMPERATURE = 0.7

    client = MagicMock()

    client.chat.completions.create.side_effect = RateLimitError(
        "Rate limit",
        response=MagicMock(),
        body=None,
    )

    mock_openai.return_value = client

    provider = OpenAIProvider()

    with pytest.raises(
        AIRateLimitError,
    ):
        provider.generate_cover_letter(
            build_request(),
        )


@patch("app.ai.openai_provider.settings")
@patch("app.ai.openai_provider.OpenAI")
def test_provider_error_translated(
    mock_openai,
    mock_settings,
):
    mock_settings.OPENAI_API_KEY = "key"
    mock_settings.OPENAI_MODEL = "gpt-5"
    mock_settings.OPENAI_TIMEOUT = 60
    mock_settings.OPENAI_MAX_TOKENS = 1200
    mock_settings.OPENAI_TEMPERATURE = 0.7

    client = MagicMock()

    client.chat.completions.create.side_effect = OpenAIError(
        "Boom",
    )

    mock_openai.return_value = client

    provider = OpenAIProvider()

    with pytest.raises(
        AIProviderError,
    ):
        provider.generate_cover_letter(
            build_request(),
        )
