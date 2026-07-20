from collections.abc import Callable
from typing import TypeVar
from uuid import UUID

from app.ai.contracts import (
    AIExecutionResult,
)
from app.ai.exceptions import (
    AIGenerationError,
    AIProviderError,
    AIRateLimitError,
    AITimeoutError,
)
from app.ai.observability.service import AIObservabilityService
from app.ai.providers import AIProvider
from app.ai.retry import RetryService
from app.ai.schemas import (
    ATSOptimizationRequest,
    ATSOptimizationResult,
    CoverLetterGenerationRequest,
    ResumeGenerationRequest,
)
from app.ats.scoring import ATSScoringService

RequestT = TypeVar("RequestT")


class AIService:
    """
    Coordinates AI generation using the configured provider.
    """

    def __init__(
        self,
        provider: AIProvider,
        retry_service: RetryService | None = None,
        observability_service: AIObservabilityService | None = None,
    ) -> None:
        self.provider = provider
        self.retry_service = retry_service
        self.observability_service = observability_service

    def _execute_generation(
        self,
        *,
        operation: str,
        request: RequestT,
        generate: Callable[
            [RequestT],
            AIExecutionResult[str],
        ],
        request_id: str | None = None,
        user_id: str | None = None,
        resume_id: UUID | None = None,
        cover_letter_id: UUID | None = None,
    ) -> AIExecutionResult[str]:
        """
        Execute an AI generation request with optional observability.
        """

        context = (
            self.observability_service.execution_started(
                provider=self.provider.provider_name,
                model=self.provider.model_name,
                prompt_version=self.provider.prompt_version,
                operation=operation,
                request_id=request_id,
                user_id=str(user_id) if user_id else None,
                resume_id=str(resume_id) if resume_id else None,
                cover_letter_id=(str(cover_letter_id) if cover_letter_id else None),
            )
            if self.observability_service is not None
            else None
        )

        try:
            if self.retry_service is None:
                result = generate(request)
            else:
                result = self.retry_service.execute(
                    generate,
                    request,
                    on_retry=lambda attempt, delay: (
                        self.observability_service.execution_retry(context)
                        if (
                            context is not None
                            and self.observability_service is not None
                        )
                        else None
                    ),
                )

        except (
            AIProviderError,
            AIGenerationError,
            AITimeoutError,
            AIRateLimitError,
        ) as exc:
            if context is not None and self.observability_service is not None:
                self.observability_service.execution_failed(
                    context,
                    exc,
                )
            raise

        if context is not None and self.observability_service is not None:
            context.attach_usage(
                prompt_tokens=result.metadata.prompt_tokens,
                completion_tokens=result.metadata.completion_tokens,
                total_tokens=result.metadata.total_tokens,
                estimated_cost=result.metadata.estimated_cost,
            )

            self.observability_service.execution_succeeded(
                context,
            )

        return result

    def generate_cover_letter(
        self,
        request: CoverLetterGenerationRequest,
        *,
        request_id: str | None = None,
        user_id: UUID | None = None,
        resume_id: UUID | None = None,
        cover_letter_id: UUID | None = None,
    ) -> AIExecutionResult[str]:
        """
        Generate a cover letter.
        """

        return self._execute_generation(
            operation="cover_letter_generation",
            request=request,
            request_id=request_id,
            user_id=user_id,
            resume_id=resume_id,
            cover_letter_id=cover_letter_id,
            generate=self.provider.generate_cover_letter,
        )

    def generate_resume(
        self,
        request: ResumeGenerationRequest,
        *,
        request_id: str | None = None,
        user_id: UUID | None = None,
        resume_id: UUID | None = None,
    ) -> AIExecutionResult[str]:
        """
        Generate a resume.
        """

        return self._execute_generation(
            operation="resume_generation",
            request=request,
            request_id=request_id,
            user_id=user_id,
            resume_id=resume_id,
            generate=self.provider.generate_resume,
        )

    def generate_ats_optimization(
        self,
        request: ATSOptimizationRequest,
        *,
        request_id: str | None = None,
        user_id: UUID | None = None,
        resume_id: UUID | None = None,
    ) -> ATSOptimizationResult:
        """
        Generate an ATS-optimized resume together with
        deterministic ATS scoring information.
        """

        result = self._execute_generation(
            operation="ats_optimization",
            request=request,
            request_id=request_id,
            user_id=user_id,
            resume_id=resume_id,
            generate=self.provider.generate_ats_optimization,
        )

        score, matched_keywords, missing_keywords = ATSScoringService.score(
            resume=result.content,
            job_description=request.job_description,
        )

        recommendations: list[str] = []

        if missing_keywords:
            recommendations.append(
                "Consider incorporating the missing ATS keywords where they " \
                "accurately reflect your experience."
            )

        if score < 80:
            recommendations.append(
                "Improve alignment between the resume and the target job description."
            )

        if score >= 80:
            recommendations.append(
                "The resume demonstrates strong ATS keyword alignment."
            )

        return ATSOptimizationResult(
            optimized_resume=result.content,
            ats_score=score,
            matched_keywords=matched_keywords,
            missing_keywords=missing_keywords,
            recommendations=recommendations,
        )
