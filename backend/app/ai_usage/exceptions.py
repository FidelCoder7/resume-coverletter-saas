class AIUsageNotFoundError(Exception):
    """
    Raised when an AI usage record cannot be found.
    """

    def __init__(
        self,
        message: str = "AI usage record not found.",
    ) -> None:
        super().__init__(
            message,
        )


class AIUsageAccessDeniedError(Exception):
    """
    Raised when a user attempts to access another user's AI usage record.
    """

    def __init__(
        self,
        message: str = "You do not have access to this AI usage record.",
    ) -> None:
        super().__init__(
            message,
        )
