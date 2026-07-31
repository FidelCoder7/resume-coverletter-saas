class ResumeExportError(Exception):
    """
    Base exception for resume export errors.
    """


class ResumeExportNotFound(ResumeExportError):
    """
    Raised when a requested resume cannot be found.
    """


class UnsupportedResumeExportFormat(ResumeExportError):
    """
    Raised when an unsupported export format is requested.
    """
