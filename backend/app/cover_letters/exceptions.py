class CoverLetterNotFound(Exception):
    """Raised when the requested cover letter does not exist."""


class CoverLetterAccessDenied(Exception):
    """Raised when a user tries to access another user's cover letter."""


class DuplicateCoverLetter(Exception):
    """Raised when a cover letter title already exists on a resume."""
