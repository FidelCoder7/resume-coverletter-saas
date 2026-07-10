from fastapi import APIRouter

from app.api.v1.router import router as v1_router
from app.educations.router import router as education_router
from app.experiences.router import router as experiences_router
from app.resumes.router import router as resumes_router
from app.skills.router import router as skills_router
from app.users.router import router as users_router

api_router = APIRouter()

api_router.include_router(
    v1_router,
    prefix="/v1",
)

api_router.include_router(
    users_router,
)

api_router.include_router(
    resumes_router,
)

api_router.include_router(
    experiences_router,
)

api_router.include_router(
    education_router,
)

api_router.include_router(
    skills_router,
)
