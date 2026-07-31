class AdminAccessDenied(Exception):
    """Raised when a non-admin user attempts to access an admin resource."""


class AdminUserNotFound(Exception):
    """Raised when an administrator requests a user that does not exist."""


class AdminUserActionNotAllowed(Exception):
    """
    Raised when an administrative user action is not allowed
    by the current account state or business rules.
    """

class AdminAuditLogNotFound(Exception):
    """Raised when an administrative audit log does not exist."""
