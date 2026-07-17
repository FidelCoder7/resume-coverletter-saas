from app.ai.contracts import AIExecutionResult
from app.ai.providers import AIProvider
from app.ai.retry import RetryService
from app.ai.schemas import (
    CoverLetterGenerationRequest,
    ResumeGenerationRequest,
)


class AIService:
    """
    Coordinates AI generation using the configured provider.
    """

    def __init__(
        self,
        provider: AIProvider,
        retry_service: RetryService | None = None,
    ) -> None:
        self.provider = provider
        self.retry_service = retry_service

    def generate_cover_letter(
        self,
        request: CoverLetterGenerationRequest,
    ) -> AIExecutionResult[str]:
        """
        Generate a cover letter.
        """

        if self.retry_service is None:
            return self.provider.generate_cover_letter(
                request,
            )

        return self.retry_service.execute(
            self.provider.generate_cover_letter,
            request,
        )

    def generate_resume(
        self,
        request: ResumeGenerationRequest,
    ) -> AIExecutionResult[str]:
        """
        Generate a resume.
        """

        if self.retry_service is None:
            return self.provider.generate_resume(
                request,
            )

        return self.retry_service.execute(
            self.provider.generate_resume,
            request,
        )
