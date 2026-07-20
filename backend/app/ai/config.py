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
    retry_initial_delay: float
    retry_backoff_multiplier: float
    retry_max_delay: float
    retry_jitter: bool

    resume_prompt_version: str
    cover_letter_prompt_version: str
    ats_optimization_prompt_version: str


ai_settings = AISettings(
    api_key=settings.OPENAI_API_KEY,
    default_provider=settings.AI_DEFAULT_PROVIDER,
    default_model=settings.OPENAI_MODEL,
    timeout=settings.OPENAI_TIMEOUT,
    max_tokens=settings.OPENAI_MAX_TOKENS,
    temperature=settings.OPENAI_TEMPERATURE,
    retry_attempts=settings.AI_RETRY_ATTEMPTS,
    retry_initial_delay=settings.AI_RETRY_INITIAL_DELAY,
    retry_backoff_multiplier=settings.AI_RETRY_BACKOFF_MULTIPLIER,
    retry_max_delay=settings.AI_RETRY_MAX_DELAY,
    retry_jitter=settings.AI_RETRY_JITTER,
    resume_prompt_version=settings.AI_RESUME_PROMPT_VERSION,
    cover_letter_prompt_version=settings.AI_COVER_LETTER_PROMPT_VERSION,
    ats_optimization_prompt_version=settings.AI_ATS_OPTIMIZATION_PROMPT_VERSION,
)
