import pytest

from app.ai.config import AISettings
from app.ai.exceptions import AIConfigurationError
from app.ai.openai_provider import OpenAIProvider
from app.ai.provider_factory import AIProviderFactory


def build_config(
    *,
    provider: str = "openai",
) -> AISettings:
    return AISettings(
        api_key="test-key",
        default_provider=provider,
        default_model="gpt-5",
        timeout=60,
        max_tokens=1200,
        temperature=0.7,
        retry_attempts=3,
        retry_backoff=1.0,
        resume_prompt_version="resume_v1",
        cover_letter_prompt_version="cover_letter_v1",
    )


def test_create_openai_provider():
    provider = AIProviderFactory.create(
        config=build_config(),
    )

    assert isinstance(
        provider,
        OpenAIProvider,
    )


def test_provider_receives_configuration():
    config = build_config()

    provider = AIProviderFactory.create(
        config=config,
    )

    assert provider.config is config


def test_unknown_provider_raises_configuration_error():
    with pytest.raises(
        AIConfigurationError,
        match="Unsupported AI provider",
    ):
        AIProviderFactory.create(
            config=build_config(
                provider="anthropic",
            ),
        )


@pytest.mark.parametrize(
    "provider",
    [
        "",
        "invalid",
        "something-else",
    ],
)
def test_invalid_provider_names_raise_configuration_error(
    provider: str,
):
    with pytest.raises(
        AIConfigurationError,
    ):
        AIProviderFactory.create(
            config=build_config(
                provider=provider,
            ),
        )


def test_provider_name_is_case_insensitive():
    provider = AIProviderFactory.create(
        config=build_config(
            provider="OPENAI",
        ),
    )

    assert isinstance(
        provider,
        OpenAIProvider,
    )
