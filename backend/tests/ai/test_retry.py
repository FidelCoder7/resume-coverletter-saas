import pytest

from app.ai.config import AISettings
from app.ai.exceptions import (
    AIGenerationError,
    AIProviderError,
    AIRateLimitError,
    AITimeoutError,
)
from app.ai.retry import RetryService


def build_config() -> AISettings:
    return AISettings(
        api_key="test-key",
        default_provider="openai",
        default_model="gpt-5",
        timeout=60,
        max_tokens=1200,
        temperature=0.7,
        retry_attempts=3,
        retry_backoff=0,
        resume_prompt_version="resume_v1",
        cover_letter_prompt_version="cover_letter_v1",
    )


def test_execute_success_first_attempt():
    retry = RetryService(
        config=build_config(),
    )

    calls = 0

    def operation():
        nonlocal calls
        calls += 1
        return "success"

    result = retry.execute(
        operation,
    )

    assert result == "success"
    assert calls == 1


def test_execute_retries_then_succeeds():
    retry = RetryService(
        config=build_config(),
    )

    calls = 0

    def operation():
        nonlocal calls
        calls += 1

        if calls < 3:
            raise AIRateLimitError(
                "Rate limit",
            )

        return "success"

    result = retry.execute(
        operation,
    )

    assert result == "success"
    assert calls == 3


def test_execute_exhausts_retries():
    retry = RetryService(
        config=build_config(),
    )

    calls = 0

    def operation():
        nonlocal calls
        calls += 1
        raise AIRateLimitError(
            "Still failing",
        )

    with pytest.raises(
        AIRateLimitError,
    ):
        retry.execute(
            operation,
        )

    assert calls == 3


def test_timeout_is_retried():
    retry = RetryService(
        config=build_config(),
    )

    calls = 0

    def operation():
        nonlocal calls
        calls += 1

        if calls < 3:
            raise AITimeoutError(
                "Timeout",
            )

        return "ok"

    result = retry.execute(
        operation,
    )

    assert result == "ok"
    assert calls == 3


def test_provider_error_is_retried():
    retry = RetryService(
        config=build_config(),
    )

    calls = 0

    def operation():
        nonlocal calls
        calls += 1

        if calls < 2:
            raise AIProviderError(
                "Temporary provider issue",
            )

        return "done"

    result = retry.execute(
        operation,
    )

    assert result == "done"
    assert calls == 2


def test_generation_error_not_retried():
    retry = RetryService(
        config=build_config(),
    )

    calls = 0

    def operation():
        nonlocal calls
        calls += 1
        raise AIGenerationError(
            "Bad prompt",
        )

    with pytest.raises(
        AIGenerationError,
    ):
        retry.execute(
            operation,
        )

    assert calls == 1


def test_execute_passes_arguments():
    retry = RetryService(
        config=build_config(),
    )

    def operation(a, b, *, c):
        return a + b + c

    result = retry.execute(
        operation,
        1,
        2,
        c=3,
    )

    assert result == 6
