class EducationNotFound(Exception):
    """
    Raised when an education record or its parent resume cannot be found.
    """

    pass


class EducationAccessDenied(Exception):
    """
    Raised when a user attempts to access or modify
    another user's education.
    """

    pass


class InvalidEducationDates(Exception):
    """
    Raised when the supplied education dates
    violate business rules.
    """

    pass
