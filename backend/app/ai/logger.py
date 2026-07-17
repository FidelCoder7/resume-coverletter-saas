import logging

logger = logging.getLogger(__name__)


class AILogger:
    """
    Centralized logger for AI operations.
    """

    @staticmethod
    def generation_started(
        *,
        provider: str,
        model: str,
        prompt_version: str,
    ) -> None:
        logger.info(
            "AI generation started.",
            extra={
                "provider": provider,
                "model": model,
                "prompt_version": prompt_version,
            },
        )

    @staticmethod
    def generation_completed(
        *,
        provider: str,
        model: str,
        latency_ms: int | None,
        total_tokens: int | None,
    ) -> None:
        logger.info(
            "AI generation completed.",
            extra={
                "provider": provider,
                "model": model,
                "latency_ms": latency_ms,
                "total_tokens": total_tokens,
            },
        )

    @staticmethod
    def generation_failed(
        *,
        provider: str,
        model: str,
        exception: Exception,
    ) -> None:
        logger.exception(
            "AI generation failed.",
            extra={
                "provider": provider,
                "model": model,
            },
        )
