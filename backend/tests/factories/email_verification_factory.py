from datetime import UTC, datetime, timedelta

from app.auth.security import (
    generate_email_verification_token,
    hash_email_verification_token,
)
from app.email_verification.models import EmailVerificationToken


def create_email_verification_token(
    db,
    *,
    user,
):
    """
    Returns:
        (raw_token, model)
    """

    raw_token = generate_email_verification_token()

    token = EmailVerificationToken(
        user_id=user.id,
        token_hash=hash_email_verification_token(raw_token),
        expires_at=datetime.now(UTC) + timedelta(hours=24),
    )

    db.add(token)
    db.commit()
    db.refresh(token)

    return raw_token, token
