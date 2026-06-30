from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.exceptions import EmailAlreadyExistsException
from app.auth.schemas import RegisterRequest
from app.auth.security import hash_password
from app.users.models import (
    AccountStatus,
    SubscriptionPlan,
    User,
    UserRole,
)


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def register(self, data: RegisterRequest) -> User:
        existing = self.db.scalar(select(User).where(User.email == data.email))

        if existing:
            raise EmailAlreadyExistsException()

        user = User(
            email=data.email,
            full_name=data.full_name,
            password_hash=hash_password(data.password),
            role=UserRole.USER,
            subscription_plan=SubscriptionPlan.FREE,
            status=AccountStatus.PENDING,
            is_email_verified=False,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user
