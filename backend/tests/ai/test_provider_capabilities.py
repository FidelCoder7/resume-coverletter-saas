from unittest.mock import patch

from app.ai.config import AISettings
from app.ai.openai_provider import OpenAIProvider


def build_config() -> AISettings:
    return AISettings(
        api_key="test-key",
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
        ats_optimization_prompt_version="ats_v1",
    )


@patch("app.ai.openai_provider.OpenAI")
def test_openai_provider_capabilities(
    mock_openai,
):
    provider = OpenAIProvider(
        config=build_config(),
    )

    capabilities = provider.capabilities

    assert capabilities.supports_cover_letters is True
    assert capabilities.supports_resume_generation is True
    assert capabilities.supports_ats_optimization is True
    assert capabilities.supports_streaming is False
    assert capabilities.supports_json_mode is False
    assert capabilities.supports_vision is False


@patch("app.ai.openai_provider.OpenAI")
def test_capabilities_are_immutable(
    mock_openai,
):
    provider = OpenAIProvider(
        config=build_config(),
    )

    capabilities = provider.capabilities

    assert capabilities == provider.capabilities
