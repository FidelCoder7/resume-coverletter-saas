class SkillAccessDenied(Exception):
    "Raised when a user tries to access a skill from another user's resume."


class SkillNotFound(Exception):
    "Raised when a skill entry in not found"
