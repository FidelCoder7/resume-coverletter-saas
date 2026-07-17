import os
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.common.constants import Environment


class Settings(BaseSettings):
    """
    Application configuration.
    """

    APP_NAME: str
    APP_VERSION: str
    APP_ENV: Environment

    DATABASE_URL: str
    TEST_DATABASE_URL: str | None = None

    SECRET_KEY: str
    REFRESH_SECRET_KEY: str

    ALGORITHM: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    EMAIL_VERIFICATION_TOKEN_EXPIRE_HOURS: int
    PASSWORD_RESET_TOKEN_EXPIRE_HOURS: int

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_HOST: str
    MAIL_PORT: int

    MAIL_STARTTLS: bool
    MAIL_SSL_TLS: bool

    MAIL_FROM: str
    MAIL_FROM_NAME: str

    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str

    FRONTEND_URL: str

    CORS_ORIGINS: list[str] = Field(
        default_factory=list,
    )

    #
    # AI Configuration
    #

    AI_DEFAULT_PROVIDER: str = "openai"

    OPENAI_API_KEY: str | None = None

    OPENAI_MODEL: str = "gpt-5"

    OPENAI_TIMEOUT: int = Field(
        default=60,
        gt=0,
    )

    OPENAI_MAX_TOKENS: int = Field(
        default=1200,
        gt=0,
    )

    OPENAI_TEMPERATURE: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
    )

    AI_RETRY_ATTEMPTS: int = Field(
        default=3,
        ge=1,
    )

    AI_RETRY_BACKOFF: float = Field(
        default=1.0,
        gt=0,
    )

    AI_RESUME_PROMPT_VERSION: str = "resume_v1"

    AI_COVER_LETTER_PROMPT_VERSION: str = "cover_letter_v1"

    model_config = SettingsConfigDict(
        env_file=os.getenv(
            "ENV_FILE",
            ".env",
        ),
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    """
    Return a cached settings instance.
    """

    return Settings()


settings = get_settings()
