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
    

    payload = {
        "sub": subject,
        "type": "access",
        "iat": datetime.now(UTC),
        "exp": datetime.now(UTC)
        + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
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

        return TokenPayload.model_validate(payload)

    except JWTInvalidTokenError as exc:
        raise InvalidToken("Invalid or expired token.") from exc
