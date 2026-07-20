from abc import ABC, abstractmethod

from app.ai.contracts import AIExecutionResult
from app.ai.provider_capabilities import ProviderCapabilities
from app.ai.schemas import (
    ATSOptimizationRequest,
    ATSOptimizationResult,
    CoverLetterGenerationRequest,
    ResumeGenerationRequest,
)


class AIProvider(ABC):
    """
    Provider-agnostic interface implemented by every AI provider.

    Each provider exposes its supported capabilities together with
    generation operations for the AI features supported by the
    application.
    """

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
        Default prompt version used by this provider.
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

    @abstractmethod
    def generate_ats_optimization(
        self,
        request: ATSOptimizationRequest,
    ) -> AIExecutionResult[ATSOptimizationResult]:
        """
        Generate an ATS-optimized version of a resume.

        This operation analyzes an existing resume against a supplied
        job description and returns an optimized resume without
        modifying any persisted data.
        """
