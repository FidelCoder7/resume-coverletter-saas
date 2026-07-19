import random
from collections.abc import Callable
from time import sleep
from typing import ParamSpec, TypeVar

from app.ai.config import AISettings
from app.ai.exceptions import (
    AIConfigurationError,
    AIGenerationError,
    AIProviderError,
)

P = ParamSpec("P")
T = TypeVar("T")


class RetryService:
    """
    Executes retryable AI operations.

    Only transient provider failures are retried. Configuration,
    validation, and generation failures are immediately propagated.
    """

    RETRYABLE_EXCEPTIONS = (AIProviderError,)

    NON_RETRYABLE_EXCEPTIONS = (
        AIConfigurationError,
        AIGenerationError,
    )

    def __init__(
        self,
        config: AISettings,
        sleeper: Callable[[float], None] = sleep,
        randomizer: Callable[[float, float], float] = random.uniform,
    ) -> None:
        self.config = config
        self._sleeper = sleeper
        self._randomizer = randomizer

    def execute(
        self,
        operation: Callable[P, T],
        *args: P.args,
        on_retry: Callable[[int, float], None] | None = None,
        **kwargs: P.kwargs,
    ) -> T:
        """
        Execute an operation using the configured retry policy.
        """

        attempts = self.config.retry_attempts

        for attempt in range(1, attempts + 1):
            try:
                return operation(
                    *args,
                    **kwargs,
                )

            except self.NON_RETRYABLE_EXCEPTIONS:
                raise

            except self.RETRYABLE_EXCEPTIONS as exc:
                if not self._should_retry(exc):
                    raise

                if attempt >= attempts:
                    raise

                delay = self._calculate_delay(
                    attempt,
                )

                delay = self._apply_jitter(
                    delay,
                )

                if on_retry is not None:
                    on_retry(attempt, delay)

                self._sleep(
                    delay,
                )

        raise RuntimeError(
            "Retry policy exhausted unexpectedly.",
        )

    def _should_retry(
        self,
        exc: Exception,
    ) -> bool:
        if isinstance(
            exc,
            self.NON_RETRYABLE_EXCEPTIONS,
        ):
            return False

        return isinstance(
            exc,
            self.RETRYABLE_EXCEPTIONS,
        )

    def _calculate_delay(
        self,
        attempt: int,
    ) -> float:
        delay = self.config.retry_initial_delay * (
            self.config.retry_backoff_multiplier ** (attempt - 1)
        )

        return min(
            delay,
            self.config.retry_max_delay,
        )

    def _apply_jitter(
        self,
        delay: float,
    ) -> float:
        if not self.config.retry_jitter:
            return delay

        return self._randomizer(
            delay * 0.8,
            delay * 1.2,
        )

    def _sleep(
        self,
        delay: float,
    ) -> None:
        self._sleeper(delay)
