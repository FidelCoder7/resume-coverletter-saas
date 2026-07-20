from uuid import UUID

from app.ai.schemas import ATSOptimizationRequest, ATSOptimizationResult
from app.ai.service import AIService
from app.ai_usage.service import AIUsageService
from app.ats.scoring import ATSScoringService
from app.common.constants import AIFeature


class ATSAIService:
    """
    Handles AI-powered ATS optimization.
    """

    def __init__(
        self,
        ai_service: AIService,
        ai_usage_service: AIUsageService,
    ) -> None:
        self.ai_service = ai_service
        self.ai_usage_service = ai_usage_service

    def optimize(
        self,
        *,
        user_id: UUID,
        resume_id: UUID,
        resume_content: str,
        job_description: str,
        target_job_title: str | None,
    ) -> ATSOptimizationResult:
        request = ATSOptimizationRequest(
            resume_content=resume_content,
            job_description=job_description,
            target_job_title=target_job_title,
        )

        
        result = self.ai_service.generate_ats_optimization(
            request,
            user_id=user_id,
            resume_id=resume_id,
        )


        score, matched, missing = ATSScoringService.score(
            resume=result.content,
            job_description=job_description,
        )

        self.ai_usage_service.record_success(
            user_id=user_id,
            resume_id=resume_id,
            feature=AIFeature.ATS_OPTIMIZATION,
            metadata=result.metadata,
        )

        return ATSOptimizationResult(
            optimized_resume=result.content,
            ats_score=score,
            matched_keywords=matched,
            missing_keywords=missing,
            recommendations=[],
        )
