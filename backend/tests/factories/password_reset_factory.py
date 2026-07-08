from datetime import UTC, datetime, timedelta

from app.auth.security import (
    generate_password_reset_token,
    hash_password_reset_token,
)
from app.password_reset.models import PasswordResetToken


def create_password_reset_token(
    db,
    *,
    user,
):
    """
    Create a password reset token.

    Returns:
        (raw_token, model)
    """

    raw_token = generate_password_reset_token()

    token = PasswordResetToken(
        user_id=user.id,
        token_hash=hash_password_reset_token(raw_token),
        expires_at=datetime.now(UTC) + timedelta(hours=1),
    )

    db.add(token)
    db.commit()
    db.refresh(token)

    return raw_token, token
