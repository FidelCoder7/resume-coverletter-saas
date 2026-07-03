from fastapi import FastAPI

import app.database.models
from app.api.router import api_router
from app.auth.router import router as auth_router
from app.core.config import settings
from app.core.lifespan import lifespan
from app.core.logging import setup_logging

setup_logging()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

app.include_router(
    api_router,
    prefix="/api",
)

app.include_router(auth_router)


@app.get("/", tags=["Root"])
async def root() -> dict[str, str]:
    return {"message": f"Welcome to {settings.APP_NAME}"}
