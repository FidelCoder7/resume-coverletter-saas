class PasswordResetTokenInvalid(Exception):
    """Raised when a password reset token is invalid."""


class PasswordResetTokenExpired(Exception):
    """Raised when a password reset token has expired."""
