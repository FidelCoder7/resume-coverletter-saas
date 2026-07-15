from abc import ABC, abstractmethod

from app.ai.contracts import AIExecutionResult
from app.ai.schemas import (
    CoverLetterGenerationRequest,
    ResumeGenerationRequest,
)


class AIProvider(ABC):
    """
    Abstract interface implemented by all AI providers.
    """

    @abstractmethod
    def generate_cover_letter(
        self,
        request: CoverLetterGenerationRequest,
    ) -> AIExecutionResult[str]:
        """
        Generate a cover letter.
        """
        raise NotImplementedError

    @abstractmethod
    def generate_resume(
        self,
        request: ResumeGenerationRequest,
    ) -> AIExecutionResult[str]:
        """
        Generate a resume.
        """
        raise NotImplementedError
