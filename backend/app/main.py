from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

import app.database.models
from app.api.router import api_router
from app.auth.router import router as auth_router
from app.core.config import settings
from app.core.exception_handlers import register_exception_handlers
from app.core.lifespan import lifespan
from app.core.logging import setup_logging
from app.core.rate_limit import limiter
from app.core.rate_limit_handler import rate_limit_handler
from app.core.security_headers import SecurityHeadersMiddleware

setup_logging()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    rate_limit_handler,
)

if settings.APP_ENV.value == "production":
    app.add_middleware(
        HTTPSRedirectMiddleware,
    )

register_exception_handlers(app)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    same_site="lax",
    https_only=settings.APP_ENV.value == "production",
    max_age=600,
)

app.add_middleware(
    SlowAPIMiddleware,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
        "OPTIONS",
    ],
    allow_headers=["*"],
)

if settings.APP_ENV.value == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=[
            "yourdomain.com",
            "www.yourdomain.com",
        ],
    )

app.add_middleware(
    SecurityHeadersMiddleware,
)

app.include_router(
    api_router,
    prefix="/api",
)

app.include_router(auth_router)


@app.get("/", tags=["Root"])
async def root() -> dict[str, str]:
    return {"message": f"Welcome to {settings.APP_NAME}"}
