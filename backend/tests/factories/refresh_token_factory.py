from datetime import UTC, datetime, timedelta

from app.auth.security import (
    create_refresh_token,
    hash_refresh_token,
)
from app.refresh_tokens.models import RefreshToken


def create_refresh_token_record(
    db,
    *,
    user,
):
    """
    Create a persisted refresh token.

    Returns:
        (raw_token, model)
    """

    raw_token = create_refresh_token(
        str(user.id),
    )

    token = RefreshToken(
        user_id=user.id,
        token_hash=hash_refresh_token(raw_token),
        expires_at=datetime.now(UTC) + timedelta(days=30),
    )

    db.add(token)
    db.commit()
    db.refresh(token)

    return raw_token, token
