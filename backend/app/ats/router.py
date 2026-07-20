from uuid import UUID

from fastapi import APIRouter, Depends

from app.ats.dependencies import get_ats_service
from app.ats.schemas import (
    ATSOptimizationRequest,
    ATSOptimizationResponse,
)
from app.ats.service import ATSService
from app.auth.dependencies import get_current_user
from app.users.models import User

router = APIRouter(
    prefix="/ats",
    tags=["ATS"],
)


@router.post(
    "/optimize/{resume_id}",
    response_model=ATSOptimizationResponse,
)
def optimize_resume(
    resume_id: UUID,
    payload: ATSOptimizationRequest,
    current_user: User = Depends(get_current_user),
    service: ATSService = Depends(get_ats_service),
):
    return service.optimize_resume(
        user_id=current_user.id,
        resume_id=resume_id,
        job_description=payload.job_description,
        target_job_title=payload.target_job_title,
    )
