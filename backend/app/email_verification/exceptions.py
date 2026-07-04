class EmailVerificationError(Exception):
    """Base email verification exception."""


class VerificationTokenInvalid(EmailVerificationError):
    """Verification token is invalid."""


class VerificationTokenExpired(EmailVerificationError):
    """Verification token has expired."""
