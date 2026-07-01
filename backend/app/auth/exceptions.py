class AuthenticationError(Exception):
    """Base exception for authentication errors."""


class InvalidCredentials(AuthenticationError):
    """Raised when email or password is incorrect."""


class InvalidToken(AuthenticationError):
    """Raised when a JWT is invalid or expired."""


class AccountInactive(AuthenticationError):
    """Raised when an account is not active."""


class EmailAlreadyRegistered(AuthenticationError):
    """Raised when attempting to register an existing email."""
