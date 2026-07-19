from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from openai import (
    APITimeoutError,
    OpenAIError,
    RateLimitError,
)

from app.ai.base_chat_provider import BaseChatProvider
from app.ai.exceptions import (
    AIGenerationError,
    AIProviderError,
    AIRateLimitError,
    AITimeoutError,
)


def build_response(
    *,
    content: str = "Generated content.",
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
            prompt_tokens=100,
            completion_tokens=150,
            total_tokens=250,
        ),
    )


class FakeChatProvider(BaseChatProvider):
    def __init__(
        self,
        response=None,
        exception=None,
    ):
        self.response = response
        self.exception = exception

    def create_completion(
        self,
        *,
        messages: list[dict[str, str]],
    ):
        if self.exception is not None:
            raise self.exception

        return self.response

    def provider_name(
        self,
    ) -> str:
        return "fake"

    def model_name(
        self,
    ) -> str:
        return "fake-model"


def test_execute_generation_success():
    provider = FakeChatProvider(
        response=build_response(),
    )

    result = provider.execute_generation(
        messages=[],
        prompt_version="test-v1",
        error_message="Provider failed.",
    )

    assert result.content == "Generated content."

    assert result.metadata.provider == "fake"
    assert result.metadata.model == "fake-model"
    assert result.metadata.prompt_version == "test-v1"

    assert result.metadata.prompt_tokens == 100
    assert result.metadata.completion_tokens == 150
    assert result.metadata.total_tokens == 250

    assert result.metadata.latency_ms is not None
    assert result.metadata.latency_ms >= 0


def test_empty_choices_raise_generation_error():
    provider = FakeChatProvider(
        response=SimpleNamespace(
            choices=[],
            usage=None,
        ),
    )

    with pytest.raises(
        AIGenerationError,
        match="returned no choices",
    ):
        provider.execute_generation(
            messages=[],
            prompt_version="test-v1",
            error_message="Provider failed.",
        )


def test_empty_content_raises_generation_error():
    provider = FakeChatProvider(
        response=build_response(
            content="",
        ),
    )

    with pytest.raises(
        AIGenerationError,
        match="empty response",
    ):
        provider.execute_generation(
            messages=[],
            prompt_version="test-v1",
            error_message="Provider failed.",
        )


def test_missing_message_raises_generation_error():
    response = build_response()

    response.choices[0].message = None

    provider = FakeChatProvider(
        response=response,
    )

    with pytest.raises(
        AIGenerationError,
        match="empty response",
    ):
        provider.execute_generation(
            messages=[],
            prompt_version="test-v1",
            error_message="Provider failed.",
        )


def test_truncated_response_raises_generation_error():
    provider = FakeChatProvider(
        response=build_response(
            finish_reason="length",
        ),
    )

    with pytest.raises(
        AIGenerationError,
        match="token limit",
    ):
        provider.execute_generation(
            messages=[],
            prompt_version="test-v1",
            error_message="Provider failed.",
        )


def test_timeout_is_translated():
    provider = FakeChatProvider(
        exception=APITimeoutError(
            request=MagicMock(),
        ),
    )

    with pytest.raises(
        AITimeoutError,
        match="timed out",
    ):
        provider.execute_generation(
            messages=[],
            prompt_version="test-v1",
            error_message="Provider failed.",
        )


def test_rate_limit_is_translated():
    provider = FakeChatProvider(
        exception=RateLimitError(
            "Rate limit",
            response=MagicMock(),
            body=None,
        ),
    )

    with pytest.raises(
        AIRateLimitError,
        match="rate limit",
    ):
        provider.execute_generation(
            messages=[],
            prompt_version="test-v1",
            error_message="Provider failed.",
        )


def test_provider_error_is_translated():
    provider = FakeChatProvider(
        exception=OpenAIError(
            "Boom",
        ),
    )

    with pytest.raises(
        AIProviderError,
        match="Provider failed.",
    ):
        provider.execute_generation(
            messages=[],
            prompt_version="test-v1",
            error_message="Provider failed.",
        )
