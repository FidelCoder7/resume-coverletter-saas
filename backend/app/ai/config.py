from dataclasses import dataclass

from app.core.config import settings


@dataclass(frozen=True, slots=True)
class AISettings:
    """
    Centralized configuration for the AI subsystem.
    """

    api_key: str | None

    default_provider: str

    default_model: str
    timeout: int
    max_tokens: int
    temperature: float

    retry_attempts: int
    retry_backoff: float

    resume_prompt_version: str
    cover_letter_prompt_version: str


ai_settings = AISettings(
    api_key=settings.OPENAI_API_KEY,
    default_provider=settings.AI_DEFAULT_PROVIDER,
    default_model=settings.OPENAI_MODEL,
    timeout=settings.OPENAI_TIMEOUT,
    max_tokens=settings.OPENAI_MAX_TOKENS,
    temperature=settings.OPENAI_TEMPERATURE,
    retry_attempts=settings.AI_RETRY_ATTEMPTS,
    retry_backoff=settings.AI_RETRY_BACKOFF,
    resume_prompt_version=settings.AI_RESUME_PROMPT_VERSION,
    cover_letter_prompt_version=settings.AI_COVER_LETTER_PROMPT_VERSION,
)
