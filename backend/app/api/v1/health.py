from fastapi import APIRouter
from sqlalchemy import text

from app.common.responses import APIResponse
from app.database.session import SessionLocal

router = APIRouter()


@router.get("/health", response_model=APIResponse)
async def health_check() -> APIResponse:
    db = SessionLocal()

    try:
        db.execute(text("SELECT 1"))

        database_status = "UP"

    except Exception:
        database_status = "DOWN"

    finally:
        db.close()

    return APIResponse(
        success=True,
        message="Application is healthy",
        data={
            "application": "UP",
            "database": database_status,
        },
    )
