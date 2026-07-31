from datetime import date, datetime
from uuid import UUID

from sqlalchemy import Date, cast, func, select
from sqlalchemy.orm import Session

from app.admin.models import AdminAuditLog
from app.common.constants import (
    AccountStatus,
    AdminAuditAction,
    SubscriptionPlan,
    UserRole,
)
from app.cover_letters.models import CoverLetter
from app.resumes.models import Resume
from app.users.models import User


class AdminUserRepository:
    """
    Repository for administrative user queries and mutations.

    Transaction boundaries are controlled by the service layer.
    Repository methods do not commit user mutations independently.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db

    def list_users(
        self,
        *,
        page: int,
        page_size: int,
        search: str | None = None,
        role: UserRole | None = None,
        status: AccountStatus | None = None,
        subscription_plan: SubscriptionPlan | None = None,
    ) -> tuple[list[User], int]:
        """
        Return a paginated list of users and the total matching count.
        """

        filters = []

        if search is not None:
            search_pattern = f"%{search.strip()}%"

            filters.append(
                
                    User.email.ilike(search_pattern)
                    | User.full_name.ilike(search_pattern)
                
            )

        if role is not None:
            filters.append(
                User.role == role,
            )

        if status is not None:
            filters.append(
                User.status == status,
            )

        if subscription_plan is not None:
            filters.append(
                User.subscription_plan == subscription_plan,
            )

        count_statement = select(
            func.count(User.id),
        )

        if filters:
            count_statement = count_statement.where(
                *filters,
            )

        total = self.db.scalar(
            count_statement,
        ) or 0

        offset = (page - 1) * page_size

        statement = (
            select(User)
            .where(*filters)
            .order_by(
                User.created_at.desc(),
                User.id.desc(),
            )
            .offset(offset)
            .limit(page_size)
        )

        users = list(
            self.db.scalars(
                statement,
            ).all()
        )

        return users, total

    def get_by_id(
        self,
        user_id: UUID,
    ) -> User | None:
        """
        Return a user by ID for administrative inspection.
        """

        statement = select(User).where(
            User.id == user_id,
        )

        return self.db.scalar(
            statement,
        )

    def suspend(
        self,
        user: User,
    ) -> User:
        """
        Mark a user account as suspended.

        The transaction is intentionally not committed here.
        """

        user.status = AccountStatus.SUSPENDED
        user.deleted_at = None

        self.db.flush()

        return user

    def reactivate(
        self,
        user: User,
    ) -> User:
        """
        Mark a user account as active.

        The transaction is intentionally not committed here.
        """

        user.status = AccountStatus.ACTIVE
        user.deleted_at = None

        self.db.flush()

        return user

    def commit(self) -> None:
        """
        Commit the current administrative transaction.
        """

        self.db.commit()

    def rollback(self) -> None:
        """
        Roll back the current administrative transaction.
        """

        self.db.rollback()


    def count_users(
        self,
        *,
        status: AccountStatus | None = None,
        role: UserRole | None = None,
        email_verified: bool | None = None,
    ) -> int:
        """
        Return the number of users matching the supplied filters.
        """

        filters = []

        if status is not None:
            filters.append(
                User.status == status,
            )

        if role is not None:
            filters.append(
                User.role == role,
            )

        if email_verified is not None:
            filters.append(
                User.is_email_verified == email_verified,
            )

        statement = select(
            func.count(User.id),
        ).where(
            *filters,
        )

        return self.db.scalar(
            statement,
        ) or 0



    def count_users_by_subscription_plan(
        self,
    ) -> dict[SubscriptionPlan, int]:
        """
        Return the number of users grouped by subscription plan.
        """

        statement = (
            select(
                User.subscription_plan,
                func.count(User.id),
            )
            .group_by(
                User.subscription_plan,
            )
        )

        results = self.db.execute(
            statement,
        ).all()

        return {
            plan: count
            for plan, count in results
        }


    def count_registrations_by_day(
        self,
        *,
        start_date: datetime,
        end_date: datetime,
    ) -> list[tuple[date, int]]:
        """
        Return user registration counts grouped by day.
        """

        statement = (
            select(
                cast(User.created_at, Date).label("date"),
                func.count(User.id).label("count"),
            )
            .where(
                User.created_at >= start_date,
                User.created_at < end_date,
            )
            .group_by(
                cast(User.created_at, Date),
            )
            .order_by(
                cast(User.created_at, Date),
            )
        )

        results = self.db.execute(
            statement,
        ).all()

        return [
            (result.date, result.count)
            for result in results
        ]
    

class AdminAuditLogRepository:
    """
    Repository responsible for administrative audit log persistence
    and read operations.

    Audit creation does not commit independently.
    The service layer owns the transaction boundary.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db

    def create(
        self,
        *,
        admin_id: UUID,
        target_user_id: UUID,
        action: AdminAuditAction,
        reason: str | None = None,
        event_metadata: dict | None = None,
    ) -> AdminAuditLog:
        """
        Add an administrative audit log to the current transaction.

        The caller is responsible for committing the transaction.
        """

        audit_log = AdminAuditLog(
            admin_id=admin_id,
            target_user_id=target_user_id,
            action=action,
            reason=reason,
            event_metadata=event_metadata,
        )

        self.db.add(audit_log)
        self.db.flush()

        return audit_log

    def get_by_id(
        self,
        audit_log_id: UUID,
    ) -> AdminAuditLog | None:
        """
        Return an audit log by ID.
        """

        statement = select(
            AdminAuditLog,
        ).where(
            AdminAuditLog.id == audit_log_id,
        )

        return self.db.scalar(
            statement,
        )

    def list_by_target_user(
        self,
        *,
        target_user_id: UUID,
        page: int,
        page_size: int,
    ) -> tuple[list[AdminAuditLog], int]:
        """
        Return audit logs for a specific target user.
        """

        filters = [
            AdminAuditLog.target_user_id == target_user_id,
        ]

        total = self.db.scalar(
            select(
                func.count(AdminAuditLog.id),
            ).where(
                *filters,
            ),
        ) or 0

        offset = (page - 1) * page_size

        statement = (
            select(AdminAuditLog)
            .where(*filters)
            .order_by(
                AdminAuditLog.created_at.desc(),
                AdminAuditLog.id.desc(),
            )
            .offset(offset)
            .limit(page_size)
        )

        logs = list(
            self.db.scalars(
                statement,
            ).all()
        )

        return logs, total

    def list_by_admin(
        self,
        *,
        admin_id: UUID,
        page: int,
        page_size: int,
    ) -> tuple[list[AdminAuditLog], int]:
        """
        Return audit logs generated by a specific administrator.
        """

        filters = [
            AdminAuditLog.admin_id == admin_id,
        ]

        total = self.db.scalar(
            select(
                func.count(AdminAuditLog.id),
            ).where(
                *filters,
            ),
        ) or 0

        offset = (page - 1) * page_size

        statement = (
            select(AdminAuditLog)
            .where(*filters)
            .order_by(
                AdminAuditLog.created_at.desc(),
                AdminAuditLog.id.desc(),
            )
            .offset(offset)
            .limit(page_size)
        )

        logs = list(
            self.db.scalars(
                statement,
            ).all()
        )

        return logs, total

    def list_recent(
        self,
        *,
        page: int,
        page_size: int,
    ) -> tuple[list[AdminAuditLog], int]:
        """
        Return the most recent administrative audit events.
        """

        total = self.db.scalar(
            select(
                func.count(AdminAuditLog.id),
            ),
        ) or 0

        offset = (page - 1) * page_size

        statement = (
            select(AdminAuditLog)
            .order_by(
                AdminAuditLog.created_at.desc(),
                AdminAuditLog.id.desc(),
            )
            .offset(offset)
            .limit(page_size)
        )

        logs = list(
            self.db.scalars(
                statement,
            ).all()
        )

        return logs, total


    def list_filtered(
        self,
        *,
        page: int,
        page_size: int,
        action: AdminAuditAction | None = None,
        admin_id: UUID | None = None,
        target_user_id: UUID | None = None,
        created_after: datetime | None = None,
        created_before: datetime | None = None,
    ) -> tuple[list[AdminAuditLog], int]:
        """
        Return paginated audit logs matching the supplied filters.
        """

        filters = []

        if action is not None:
            filters.append(
                AdminAuditLog.action == action,
            )

        if admin_id is not None:
            filters.append(
                AdminAuditLog.admin_id == admin_id,
            )

        if target_user_id is not None:
            filters.append(
                AdminAuditLog.target_user_id == target_user_id,
            )

        if created_after is not None:
            filters.append(
                AdminAuditLog.created_at >= created_after,
            )

        if created_before is not None:
            filters.append(
                AdminAuditLog.created_at <= created_before,
            )

        count_statement = select(
            func.count(AdminAuditLog.id),
        )

        if filters:
            count_statement = count_statement.where(
                *filters,
            )

        total = self.db.scalar(
            count_statement,
        ) or 0

        offset = (page - 1) * page_size

        statement = (
            select(AdminAuditLog)
            .where(*filters)
            .order_by(
                AdminAuditLog.created_at.desc(),
                AdminAuditLog.id.desc(),
            )
            .offset(offset)
            .limit(page_size)
        )

        logs = list(
            self.db.scalars(
                statement,
            ).all()
        )

        return logs, total


    def count_all(self) -> int:
        """
        Return the total number of administrative audit logs.
        """

        statement = select(
            func.count(AdminAuditLog.id),
        )

        return self.db.scalar(
            statement,
        ) or 0



    def count_audit_activity_by_day(
        self,
        *,
        start_date: datetime,
        end_date: datetime,
    ) -> list[tuple[date, int]]:
        """
        Return administrative audit activity grouped by day.
        """

        statement = (
            select(
                cast(
                    AdminAuditLog.created_at,
                    Date,
                ).label("date"),
                func.count(
                    AdminAuditLog.id,
                ).label("count"),
            )
            .where(
                AdminAuditLog.created_at >= start_date,
                AdminAuditLog.created_at < end_date,
            )
            .group_by(
                cast(
                    AdminAuditLog.created_at,
                    Date,
                ),
            )
            .order_by(
                cast(
                    AdminAuditLog.created_at,
                    Date,
                ),
            )
        )

        results = self.db.execute(
            statement,
        ).all()

        return [
            (result.date, result.count)
            for result in results
        ]



class AdminContentRepository:
    """
    Repository for administrative platform content metrics.

    
    This repository provides read-only aggregate queries for resumes
    and cover letters.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db

    def count_resumes(self) -> int:
        """
        Return the total number of resumes.
        """

        statement = select(
            func.count(Resume.id),
        )

        return self.db.scalar(
            statement,
        ) or 0

    def count_generated_resumes(self) -> int:
        """
        Return the number of resumes with generated AI content.
        """

        statement = select(
            func.count(Resume.id),
        ).where(
            Resume.generated_content.is_not(None),
        )

        return self.db.scalar(
            statement,
        ) or 0

    def count_cover_letters(self) -> int:
        """
        Return the total number of cover letters.
        """

        statement = select(
            func.count(CoverLetter.id),
        )

        return self.db.scalar(
            statement,
        ) or 0
