from fastapi import APIRouter

from app.common.responses import APIResponse

router = APIRouter()


@router.get("/health", response_model=APIResponse)
async def health_check() -> APIResponse:
    return APIResponse(
        success=True,
        message="Application is healthy",
        data={
            "status": "UP",
            "version": "1.0.0",
        },
    )
