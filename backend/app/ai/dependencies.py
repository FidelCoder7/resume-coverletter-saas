from app.ai.openai_provider import OpenAIProvider
from app.ai.providers import AIProvider
from app.ai.service import AIService


def get_ai_provider() -> AIProvider:
    """
    Return the configured AI provider.
    """

    return OpenAIProvider()


def get_ai_service() -> AIService:
    """
    Return the AI service.
    """

    provider = get_ai_provider()

    return AIService(
        provider=provider,
    )
