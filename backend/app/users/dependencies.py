from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.email_verification.repository import EmailVerificationRepository
from app.users.repository import UserRepository
from app.users.service import UserService


def get_user_service(
    db: Session = Depends(get_db),
) -> UserService:
    return UserService(
        repository=UserRepository(db),
        verification_repository=EmailVerificationRepository(db),
    )
