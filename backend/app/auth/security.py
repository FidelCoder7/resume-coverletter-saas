from datetime import UTC, datetime, timedelta

import jwt
from jwt.exceptions import InvalidTokenError as JWTInvalidTokenError
from pwdlib import PasswordHash

from app.auth.exceptions import InvalidToken
from app.auth.schemas import TokenPayload
from app.core.config import settings

# ------------------------------------------------------------------
# Password Hashing
# ------------------------------------------------------------------

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Hash a plaintext password using Argon2id."""
    return password_hash.hash(password)


def verify_password(
    password: str,
    hashed_password: str,
) -> bool:
    """Verify a plaintext password."""
    return password_hash.verify(password, hashed_password)


# ------------------------------------------------------------------
# JWT
# ------------------------------------------------------------------


def create_access_token(subject: str) -> str:
    """
    Create a signed JWT access token.
    """

    now = datetime.now(UTC)

    payload = {
        "sub": subject,
        "type": "access",
        "iat": now,
        "exp": now
        + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        ),
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def create_refresh_token(subject: str) -> str:
    """
    Create a signed refresh token.
    """

    now = datetime.now(UTC)

    payload = {
        "sub": subject,
        "type": "refresh",
        "iat": now,
        "exp": now
        + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS,
        ),
    }

    return jwt.encode(
        payload,
        settings.REFRESH_SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def decode_access_token(token: str) -> TokenPayload:
    """
    Decode and validate a JWT token.
    """

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        token_payload = TokenPayload.model_validate(payload)

        if token_payload.type != "access":
            raise InvalidToken("Invalid token type.")

        return token_payload

    except JWTInvalidTokenError as exc:
        raise InvalidToken("Invalid or expired token.") from exc


def decode_refresh_token(token: str) -> TokenPayload:
    """
    Decode and validate a refresh token.
    """

    try:
        payload = jwt.decode(
            token,
            settings.REFRESH_SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        token_payload = TokenPayload.model_validate(payload)

        if token_payload.type != "refresh":
            raise InvalidToken("Invalid token type.")

        return token_payload

    except JWTInvalidTokenError as exc:
        raise InvalidToken("Invalid or expired refresh token.") from exc
