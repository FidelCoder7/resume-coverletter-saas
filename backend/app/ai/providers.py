from abc import ABC, abstractmethod

from app.ai.schemas import (
    CoverLetterGenerationRequest,
    CoverLetterGenerationResponse,
)


class AIProvider(ABC):
    """
    Abstract interface implemented by all AI providers.

    Every provider is responsible for converting a
    CoverLetterGenerationRequest into a validated
    CoverLetterGenerationResponse.

    Implementations may call OpenAI, Anthropic, Gemini,
    Azure OpenAI, local LLMs, or any future provider.
    """

    @abstractmethod
    def generate_cover_letter(
        self,
        request: CoverLetterGenerationRequest,
    ) -> CoverLetterGenerationResponse:
        """
        Generate a cover letter from the supplied request.

        Args:
            request:
                Structured input used by the provider.

        Returns:
            A generated cover letter.

        Raises:
            AIProviderError:
                If the provider cannot generate a response.
        """
        raise NotImplementedError
