class ExperienceNotFound(Exception):
    """Raised when an experience entry cannot be found."""


class ExperienceAccessDenied(Exception):
    """Raised when a user tries to access an experience from another user's resume."""
