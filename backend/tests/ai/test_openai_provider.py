from unittest.mock import patch

import pytest

from app.ai.config import AISettings
from app.ai.exceptions import (
    AIConfigurationError,
)
from app.ai.openai_provider import OpenAIProvider


def build_config(
    *,
    api_key: str | None = "test-key",
) -> AISettings:
    return AISettings(
        api_key=api_key,
        default_provider="openai",
        default_model="gpt-5",
        timeout=60,
        max_tokens=1200,
        temperature=0.7,
        retry_attempts=3,
        retry_initial_delay=1.0,
        retry_backoff_multiplier=2.0,
        retry_max_delay=8.0,
        retry_jitter=False,
        resume_prompt_version="resume_v1",
        cover_letter_prompt_version="cover_letter_v1",
        ats_optimization_prompt_version="ats_optimization_v1",
    )


@patch("app.ai.openai_provider.OpenAI")
def test_creates_openai_client(
    mock_openai,
):
    provider = OpenAIProvider(
        config=build_config(),
    )

    mock_openai.assert_called_once_with(
        api_key="test-key",
        timeout=60,
    )

    assert provider.client is mock_openai.return_value


def test_missing_api_key_raises_configuration_error():
    with pytest.raises(
        AIConfigurationError,
    ):
        OpenAIProvider(
            config=build_config(
                api_key=None,
            ),
        )
