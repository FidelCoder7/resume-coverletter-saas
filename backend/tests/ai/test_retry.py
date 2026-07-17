import pytest

from app.ai.config import AISettings
from app.ai.exceptions import (
    AIGenerationError,
    AIProviderError,
    AIRateLimitError,
    AITimeoutError,
)
from app.ai.retry import RetryService


def build_config(
    *,
    retry_attempts: int = 3,
    retry_initial_delay: float = 1.0,
    retry_backoff_multiplier: float = 2.0,
    retry_max_delay: float = 8.0,
    retry_jitter: bool = False,
) -> AISettings:
    return AISettings(
        api_key="test-key",
        default_provider="openai",
        default_model="gpt-5",
        timeout=60,
        max_tokens=1200,
        temperature=0.7,
        retry_attempts=retry_attempts,
        retry_initial_delay=retry_initial_delay,
        retry_backoff_multiplier=retry_backoff_multiplier,
        retry_max_delay=retry_max_delay,
        retry_jitter=retry_jitter,
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

def test_calculate_delay_is_exponential():
    retry = RetryService(
        config=build_config(),
    )

    assert retry._calculate_delay(1) == 1.0
    assert retry._calculate_delay(2) == 2.0
    assert retry._calculate_delay(3) == 4.0


def test_calculate_delay_respects_max_delay():
    retry = RetryService(
        config=build_config(
            retry_max_delay=3.0,
        ),
    )

    assert retry._calculate_delay(1) == 1.0
    assert retry._calculate_delay(2) == 2.0
    assert retry._calculate_delay(3) == 3.0
    assert retry._calculate_delay(4) == 3.0


def test_apply_jitter_disabled_returns_same_delay():
    retry = RetryService(
        config=build_config(),
    )

    assert retry._apply_jitter(5.0) == 5.0


def test_sleep_uses_injected_sleeper():
    delays = []

    retry = RetryService(
        config=build_config(),
        sleeper=delays.append,
    )

    retry._sleep(2.5)

    assert delays == [2.5]


def test_execute_uses_calculated_delay():
    delays = []

    retry = RetryService(
        config=build_config(),
        sleeper=delays.append,
    )

    calls = 0

    def operation():
        nonlocal calls
        calls += 1

        if calls < 3:
            raise AIRateLimitError(
                "retry",
            )

        return "ok"

    assert retry.execute(operation) == "ok"

    assert delays == [
        1.0,
        2.0,
    ]


def test_should_retry():
    retry = RetryService(
        config=build_config(),
    )

    assert retry._should_retry(
        AIRateLimitError("x"),
    )

    assert retry._should_retry(
        AIProviderError("x"),
    )

    assert not retry._should_retry(
        AIGenerationError("x"),
    )