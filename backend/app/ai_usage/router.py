from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.ai_usage.dependencies import get_ai_usage_service
from app.ai_usage.schemas import (
    AIFeatureUsage,
    AIUsageDashboard,
    AIUsageListResponse,
    AIUsageResponse,
    AIUsageSummary,
)
from app.ai_usage.service import AIUsageService
from app.auth.dependencies import get_current_user
from app.users.models import User

router = APIRouter(
    prefix="/ai-usage",
    tags=["AI Usage"],
)


@router.get(
    "",
    response_model=AIUsageListResponse,
)
def list_user_usage(
    current_user: User = Depends(get_current_user),
    service: AIUsageService = Depends(get_ai_usage_service),
) -> AIUsageListResponse:
    """
    Return the current user's complete AI usage history.
    """

    return AIUsageListResponse(
        items=service.list_user_history(
            user_id=current_user.id,
        ),
    )


@router.get(
    "/resume/{resume_id}",
    response_model=AIUsageListResponse,
)
def list_resume_usage(
    resume_id: UUID,
    current_user: User = Depends(get_current_user),
    service: AIUsageService = Depends(get_ai_usage_service),
) -> AIUsageListResponse:
    """
    Return AI usage history associated with a resume.
    """

    items = service.list_resume_history(
        resume_id=resume_id,
    )

    user_items = [usage for usage in items if usage.user_id == current_user.id]

    return AIUsageListResponse(
        items=user_items,
    )


@router.get(
    "/cover-letter/{cover_letter_id}",
    response_model=AIUsageListResponse,
)
def list_cover_letter_usage(
    cover_letter_id: UUID,
    current_user: User = Depends(get_current_user),
    service: AIUsageService = Depends(get_ai_usage_service),
) -> AIUsageListResponse:
    """
    Return AI usage history associated with a cover letter.
    """

    items = service.list_cover_letter_history(
        cover_letter_id=cover_letter_id,
    )

    user_items = [usage for usage in items if usage.user_id == current_user.id]

    return AIUsageListResponse(
        items=user_items,
    )


@router.get(
    "/summary",
    response_model=AIUsageSummary,
)
def get_usage_summary(
    start_date: datetime = Query(...),
    end_date: datetime = Query(...),
    current_user: User = Depends(get_current_user),
    service: AIUsageService = Depends(get_ai_usage_service),
) -> AIUsageSummary:
    """
    Return aggregated AI usage statistics for the current user.
    """

    if start_date >= end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_date must be earlier than end_date.",
        )

    return service.get_usage_summary(
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date,
    )


@router.get(
    "/features",
    response_model=list[AIFeatureUsage],
)
def get_feature_breakdown(
    start_date: datetime = Query(...),
    end_date: datetime = Query(...),
    current_user: User = Depends(get_current_user),
    service: AIUsageService = Depends(get_ai_usage_service),
) -> list[AIFeatureUsage]:
    """
    Return AI usage grouped by feature.
    """

    if start_date >= end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_date must be earlier than end_date.",
        )

    return service.get_feature_breakdown(
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date,
    )


@router.get(
    "/dashboard",
    response_model=AIUsageDashboard,
)
def get_usage_dashboard(
    start_date: datetime = Query(...),
    end_date: datetime = Query(...),
    current_user: User = Depends(get_current_user),
    service: AIUsageService = Depends(get_ai_usage_service),
) -> AIUsageDashboard:
    """
    Return the complete AI usage dashboard for the current user.
    """

    if start_date >= end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_date must be earlier than end_date.",
        )

    return service.get_dashboard(
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date,
    )


@router.get(
    "/{usage_id}",
    response_model=AIUsageResponse,
)
def get_usage(
    usage_id: UUID,
    current_user: User = Depends(get_current_user),
    service: AIUsageService = Depends(get_ai_usage_service),
) -> AIUsageResponse:
    """
    Return one AI usage record belonging to the current user.
    """

    usage = service.get_usage(
        usage_id=usage_id,
    )

    if usage is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AI usage record not found.",
        )

    if usage.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this AI usage record.",
        )

    return usage
