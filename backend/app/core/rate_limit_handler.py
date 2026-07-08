from fastapi.requests import Request
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded


async def rate_limit_handler(
    request: Request,
    exc: RateLimitExceeded,
):
    return JSONResponse(
        status_code=429,
        content={
            "detail": "Too many requests. Please try again later.",
        },
    )
