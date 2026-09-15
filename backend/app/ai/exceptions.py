from app.ai.contracts import AIExecutionMetadata


class AIError(Exception):
    """
    Base exception for all AI-related errors.
    """

    def __init__(
        self,
        message: str,
        *,
        metadata: AIExecutionMetadata | None = None,
    ) -> None:
        super().__init__(message)
        self.metadata = metadata


class AIConfigurationError(AIError):
    """
    Raised when the AI provider is incorrectly configured.
    """

    pass


class AIProviderError(AIError):
    """
    Raised when the underlying AI provider fails.
    """

    pass


class AITimeoutError(AIProviderError):
    """
    Raised when an AI request exceeds the configured timeout.
    """

    pass


class AIRateLimitError(AIProviderError):
    """
    Raised when the AI provider rejects a request because the
    rate limit has been exceeded.
    """

    pass


class AIResponseError(AIProviderError):
    """
    Raised when the provider returns an invalid or malformed
    response.
    """

    pass


class AIGenerationError(AIProviderError):
    """
    Raised when an AI generation request cannot be completed
    successfully.
    """

    pass
