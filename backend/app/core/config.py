from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.common.constants import Environment


class Settings(BaseSettings):
    """Application configuration."""

    APP_NAME: str
    APP_VERSION: str
    APP_ENV: Environment

    DATABASE_URL: str

    SECRET_KEY: str
    REFRESH_SECRET_KEY: str

    ALGORITHM: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    EMAIL_VERIFICATION_TOKEN_EXPIRE_HOURS: int

    FRONTEND_URL: str
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_HOST: str
    MAIL_PORT: int

    MAIL_STARTTLS: bool
    MAIL_SSL_TLS: bool

    MAIL_FROM: str
    MAIL_FROM_NAME: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    """Return a cached settings instance."""
    return Settings()


settings = get_settings()
