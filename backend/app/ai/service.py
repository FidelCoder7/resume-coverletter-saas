from app.ai.providers import AIProvider
from app.ai.schemas import (
    CoverLetterGenerationRequest,
    CoverLetterGenerationResponse,
)


class AIService:
    """
    Coordinates AI generation using the configured provider.
    """

    def __init__(
        self,
        provider: AIProvider,
    ):
        self.provider = provider

    def generate_cover_letter(
        self,
        request: CoverLetterGenerationRequest,
    ) -> CoverLetterGenerationResponse:
        """
        Generate a cover letter.
        """

        return self.provider.generate_cover_letter(
            request,
        )
