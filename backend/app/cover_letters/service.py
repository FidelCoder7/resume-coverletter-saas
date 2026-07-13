from decimal import Decimal
from uuid import UUID

from app.ai.contracts import AIExecutionResult
from app.ai.formatters import ResumeFormatter
from app.ai.schemas import CoverLetterGenerationRequest
from app.ai.service import AIService
from app.ai_usage.models import AIUsage
from app.ai_usage.repository import AIUsageRepository
from app.common.constants import (
    AIFeature,
    AIRequestStatus,
)
from app.cover_letters.exceptions import (
    CoverLetterAccessDenied,
    CoverLetterNotFound,
)
from app.cover_letters.models import CoverLetter
from app.cover_letters.repository import CoverLetterRepository
from app.resumes.repository import ResumeRepository


class CoverLetterService:
    """
    Business logic for resume cover letter management.
    """

    def __init__(
        self,
        repository: CoverLetterRepository,
        resume_repository: ResumeRepository,
        ai_service: AIService,
        ai_usage_repository: AIUsageRepository,
    ):
        self.repository = repository
        self.resume_repository = resume_repository
        self.ai_service = ai_service
        self.ai_usage_repository = ai_usage_repository

    def _record_ai_usage(
        self,
        *,
        user_id: UUID,
        resume_id: UUID,
        cover_letter_id: UUID | None,
        feature: AIFeature,
        result: AIExecutionResult[str],
    ) -> None:
        """
        Persist telemetry for a successful AI request.
        """

        metadata = result.metadata

        usage = AIUsage(
            user_id=user_id,
            resume_id=resume_id,
            cover_letter_id=cover_letter_id,
            feature=feature,
            provider=metadata.provider,
            model=metadata.model,
            prompt_version=metadata.prompt_version,
            prompt_tokens=metadata.prompt_tokens,
            completion_tokens=metadata.completion_tokens,
            total_tokens=metadata.total_tokens,
            estimated_cost=Decimal("0"),
            latency_ms=metadata.latency_ms,
            status=AIRequestStatus.SUCCESS,
            error_message=None,
        )

        self.ai_usage_repository.create(
            usage,
        )

    def _verify_resume_owner(
        self,
        *,
        resume_id: UUID,
        user_id: UUID,
    ):
        resume = self.resume_repository.get_by_id(
            resume_id,
        )

        if resume is None:
            raise CoverLetterNotFound(
                "Resume not found.",
            )

        if resume.user_id != user_id:
            raise CoverLetterAccessDenied(
                "You do not have permission to access this resume.",
            )

        return resume

    def create_cover_letter(
        self,
        *,
        user_id: UUID,
        resume_id: UUID,
        title: str,
        company_name: str,
        job_title: str,
        content: str,
    ) -> CoverLetter:
        self._verify_resume_owner(
            resume_id=resume_id,
            user_id=user_id,
        )

        cover_letter = CoverLetter(
            resume_id=resume_id,
            title=title,
            company_name=company_name,
            job_title=job_title,
            content=content,
        )

        return self.repository.create(
            cover_letter,
        )

    def list_cover_letters(
        self,
        *,
        user_id: UUID,
        resume_id: UUID,
    ) -> list[CoverLetter]:
        self._verify_resume_owner(
            resume_id=resume_id,
            user_id=user_id,
        )

        return self.repository.list_by_resume(
            resume_id,
        )

    def get_cover_letter(
        self,
        *,
        user_id: UUID,
        cover_letter_id: UUID,
    ) -> CoverLetter:
        cover_letter = self.repository.get_by_id(
            cover_letter_id,
        )

        if cover_letter is None:
            raise CoverLetterNotFound(
                "Cover letter not found.",
            )

        self._verify_resume_owner(
            resume_id=cover_letter.resume_id,
            user_id=user_id,
        )

        return cover_letter

    def update_cover_letter(
        self,
        *,
        user_id: UUID,
        cover_letter_id: UUID,
        title: str,
        company_name: str,
        job_title: str,
        content: str,
    ) -> CoverLetter:
        cover_letter = self.get_cover_letter(
            user_id=user_id,
            cover_letter_id=cover_letter_id,
        )

        cover_letter.title = title
        cover_letter.company_name = company_name
        cover_letter.job_title = job_title
        cover_letter.content = content

        return self.repository.update(
            cover_letter,
        )

    def delete_cover_letter(
        self,
        *,
        user_id: UUID,
        cover_letter_id: UUID,
    ) -> None:
        cover_letter = self.get_cover_letter(
            user_id=user_id,
            cover_letter_id=cover_letter_id,
        )

        self.repository.delete(
            cover_letter,
        )

    def generate_cover_letter(
        self,
        *,
        user_id: UUID,
        resume_id: UUID,
        title: str,
        company_name: str,
        job_title: str,
        job_description: str,
    ) -> CoverLetter:
        resume = self._verify_resume_owner(
            resume_id=resume_id,
            user_id=user_id,
        )

        ai_request = CoverLetterGenerationRequest(
            company_name=company_name,
            job_title=job_title,
            job_description=job_description,
            resume_content=ResumeFormatter.format(
                resume,
            ),
        )

        ai_result = self.ai_service.generate_cover_letter(
            ai_request,
        )

        cover_letter = CoverLetter(
            resume_id=resume.id,
            title=title,
            company_name=company_name,
            job_title=job_title,
            content=ai_result.content,
        )

        cover_letter = self.repository.create(
            cover_letter,
        )

        self._record_ai_usage(
            user_id=user_id,
            resume_id=resume.id,
            cover_letter_id=cover_letter.id,
            feature=AIFeature.COVER_LETTER_GENERATION,
            result=ai_result,
        )

        return cover_letter

    def regenerate_cover_letter(
        self,
        *,
        user_id: UUID,
        cover_letter_id: UUID,
        job_description: str,
    ) -> CoverLetter:
        cover_letter = self.get_cover_letter(
            user_id=user_id,
            cover_letter_id=cover_letter_id,
        )

        resume = self._verify_resume_owner(
            resume_id=cover_letter.resume_id,
            user_id=user_id,
        )

        ai_request = CoverLetterGenerationRequest(
            company_name=cover_letter.company_name,
            job_title=cover_letter.job_title,
            job_description=job_description,
            resume_content=ResumeFormatter.format(
                resume,
            ),
        )

        ai_result = self.ai_service.generate_cover_letter(
            ai_request,
        )

        cover_letter.content = ai_result.content

        cover_letter = self.repository.update(
            cover_letter,
        )

        self._record_ai_usage(
            user_id=user_id,
            resume_id=resume.id,
            cover_letter_id=cover_letter.id,
            feature=AIFeature.COVER_LETTER_REGENERATION,
            result=ai_result,
        )

        return cover_letter
