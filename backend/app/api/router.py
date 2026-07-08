from fastapi import APIRouter

from app.api.v1.router import router as v1_router
from app.users.router import router as users_router

api_router = APIRouter()

api_router.include_router(
    v1_router,
    prefix="/v1",
)

api_router.include_router(
    users_router,
)
