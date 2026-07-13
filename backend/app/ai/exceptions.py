class AIError(Exception):
    """
    Base exception for all AI-related errors.
    """

    pass


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
    Raised when a cover letter cannot be generated successfully.
    """

    pass
