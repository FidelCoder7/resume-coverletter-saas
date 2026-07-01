class EmailAlreadyExistsError(Exception):
    """Raised when attempting to register with an existing email."""

    pass


class InvalidCredentialsError(Exception):
    """Raised when authentication fails."""

    pass


class UserNotFoundError(Exception):
    """Raised when a user cannot be found."""

    pass
