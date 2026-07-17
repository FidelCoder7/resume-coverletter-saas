from app.ai.config import ai_settings
from app.ai.provider_factory import AIProviderFactory
from app.ai.providers import AIProvider
from app.ai.retry import RetryService
from app.ai.service import AIService


def get_ai_provider() -> AIProvider:
    """
    Return the configured AI provider.
    """

    return AIProviderFactory.create(
        config=ai_settings,
    )


def get_ai_service() -> AIService:
    """
    Return the AI service.
    """

    provider = get_ai_provider()
    retry_service = get_retry_service()

    return AIService(
        provider=provider,
        retry_service=retry_service,
    )


def get_retry_service() -> RetryService:
    """
    Return the AI retry service.
    """

    return RetryService(
        config=ai_settings,
    )
