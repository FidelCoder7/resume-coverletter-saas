from collections.abc import Callable
from time import sleep
from typing import ParamSpec, TypeVar

from app.ai.config import AISettings
from app.ai.exceptions import (
    AIConfigurationError,
    AIGenerationError,
    AIProviderError,
    AIRateLimitError,
    AITimeoutError,
)

P = ParamSpec("P")
T = TypeVar("T")


class RetryService:
    """
    Executes retryable AI operations.

    Only transient provider failures are retried. Configuration,
    validation, and generation failures are immediately propagated.
    """

    RETRYABLE_EXCEPTIONS = (
        AITimeoutError,
        AIRateLimitError,
        AIProviderError,
    )

    NON_RETRYABLE_EXCEPTIONS = (
        AIConfigurationError,
        AIGenerationError,
    )

    def __init__(
        self,
        config: AISettings,
    ) -> None:
        self.config = config

    def execute(
        self,
        operation: Callable[P, T],
        *args: P.args,
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

            except self.RETRYABLE_EXCEPTIONS:
                if attempt >= attempts:
                    raise

                sleep(
                    self.config.retry_backoff * attempt,
                )

        raise RuntimeError(
            "Retry policy exhausted unexpectedly.",
        )
