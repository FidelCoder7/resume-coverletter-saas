from unittest.mock import patch

from app.ai.logger import AILogger


@patch("app.ai.logger.logger")
def test_generation_started(mock_logger):
    AILogger.generation_started(
        provider="openai",
        model="gpt-5",
        prompt_version="resume_v1",
    )

    mock_logger.info.assert_called_once_with(
        "AI generation started.",
        extra={
            "provider": "openai",
            "model": "gpt-5",
            "prompt_version": "resume_v1",
        },
    )


@patch("app.ai.logger.logger")
def test_generation_completed(mock_logger):
    AILogger.generation_completed(
        provider="openai",
        model="gpt-5",
        latency_ms=250,
        total_tokens=300,
    )

    mock_logger.info.assert_called_once_with(
        "AI generation completed.",
        extra={
            "provider": "openai",
            "model": "gpt-5",
            "latency_ms": 250,
            "total_tokens": 300,
        },
    )


@patch("app.ai.logger.logger")
def test_generation_failed(mock_logger):
    exc = RuntimeError("Boom")

    AILogger.generation_failed(
        provider="openai",
        model="gpt-5",
        exception=exc,
    )

    mock_logger.exception.assert_called_once_with(
        "AI generation failed.",
        extra={
            "provider": "openai",
            "model": "gpt-5",
        },
    )
