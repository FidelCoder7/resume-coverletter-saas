from abc import ABC, abstractmethod

from app.ai.contracts import AIExecutionResult
from app.ai.provider_capabilities import ProviderCapabilities
from app.ai.schemas import (
    CoverLetterGenerationRequest,
    ResumeGenerationRequest,
)


class AIProvider(ABC):

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """
        Human-readable provider identifier.
        """

    @property
    @abstractmethod
    def model_name(self) -> str:
        """
        Default model used by this provider.
        """

    @property
    @abstractmethod
    def prompt_version(self) -> str:
        """
        Current prompt version used by this provider.
        """

    @property
    @abstractmethod
    def capabilities(
        self,
    ) -> ProviderCapabilities:
        """
        Return the provider capabilities.
        """

    @abstractmethod
    def generate_cover_letter(
        self,
        request: CoverLetterGenerationRequest,
    ) -> AIExecutionResult[str]:
        """
        Generate a cover letter.
        """

    @abstractmethod
    def generate_resume(
        self,
        request: ResumeGenerationRequest,
    ) -> AIExecutionResult[str]:
        """
        Generate a resume.
        """
