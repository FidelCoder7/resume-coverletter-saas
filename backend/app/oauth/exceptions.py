class GoogleAuthenticationFailed(Exception):
    """Raised when Google OAuth authentication fails."""


class GoogleAuthorizationCancelled(Exception):
    """Raised when the user cancels Google authentication."""


class GoogleEmailNotAvailable(Exception):
    """Raised when Google does not return an email address."""


class GoogleEmailNotVerified(Exception):
    """Raised when the Google email is not verified."""
