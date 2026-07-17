from app.ai.config import AISettings
from app.ai.exceptions import AIConfigurationError
from app.ai.openai_provider import OpenAIProvider
from app.ai.providers import AIProvider


class AIProviderFactory:
    """
    Factory responsible for constructing AI provider implementations.
    """

    @staticmethod
    def create(
        config: AISettings,
    ) -> AIProvider:
        """
        Create the configured AI provider.
        """

        match config.default_provider.lower():
            case "openai":
                return OpenAIProvider(
                    config=config,
                )

            case _:
                raise AIConfigurationError(
                    f"Unsupported AI provider: {config.default_provider}",
                )
