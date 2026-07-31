class ResumeExportError(Exception):
    """
    Base exception for resume export errors.
    """


class ResumeExportNotFound(ResumeExportError):
    """
    Raised when a requested resume cannot be found.
    """

    def __init__(
        self,
        message: str = "Resume not found.",
    ) -> None:
        super().__init__(message)


class UnsupportedResumeExportFormat(ResumeExportError):
    """
    Raised when an unsupported export format is requested.
    """

    def __init__(
        self,
        message: str = "Unsupported resume export format.",
    ) -> None:
        super().__init__(message)
