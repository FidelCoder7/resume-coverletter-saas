class ResumeVersionException(Exception):
    """Base exception for resume versioning errors."""


class ResumeVersionNotFound(ResumeVersionException):
    """Raised when a requested resume version does not exist."""


class DuplicateResumeVersion(ResumeVersionException):
    """Raised when a duplicate resume version number is detected."""


class InvalidResumeVersionOperation(ResumeVersionException):
    """Raised when an invalid resume version operation is attempted."""
