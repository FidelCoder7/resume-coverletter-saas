class ResumeNotFound(Exception):
    """Raised when a resume cannot be found."""


class ResumeAccessDenied(Exception):
    """Raised when a user attempts to access another user's resume."""
