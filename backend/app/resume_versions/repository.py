from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.common.constants import ResumeVersionSource
from app.resume_versions.exceptions import DuplicateResumeVersion
from app.resume_versions.models import ResumeVersion


class ResumeVersionRepository:
    """
    Repository for resume version persistence.

    Repositories do not commit or rollback transactions.
    Transaction ownership belongs to the service layer.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        self.session = session

    def create(
        self,
        *,
        resume_id: UUID,
        version_number: int,
        snapshot: dict,
        source: ResumeVersionSource,
        change_summary: str | None = None,
    ) -> ResumeVersion:
        version = ResumeVersion(
            resume_id=resume_id,
            version_number=version_number,
            snapshot=snapshot,
            source=source,
            change_summary=change_summary,
        )

        self.session.add(version)

        try:
            self.session.flush()
        except IntegrityError as exc:
            raise DuplicateResumeVersion(
                "A resume version with this version number already exists."
            ) from exc

        return version

    def get_by_id(
        self,
        *,
        version_id: UUID,
    ) -> ResumeVersion | None:
        result = self.session.execute(
            select(ResumeVersion).where(
                ResumeVersion.id == version_id,
            )
        )

        return result.scalar_one_or_none()

    def get_by_resume_and_id(
        self,
        *,
        resume_id: UUID,
        version_id: UUID,
    ) -> ResumeVersion | None:
        """
        Return a version only when it belongs to the requested resume.
        """

        result = self.session.execute(
            select(ResumeVersion).where(
                ResumeVersion.id == version_id,
                ResumeVersion.resume_id == resume_id,
            )
        )

        return result.scalar_one_or_none()

    def get_by_resume_and_number(
        self,
        *,
        resume_id: UUID,
        version_number: int,
    ) -> ResumeVersion | None:
        result = self.session.execute(
            select(ResumeVersion).where(
                ResumeVersion.resume_id == resume_id,
                ResumeVersion.version_number == version_number,
            )
        )

        return result.scalar_one_or_none()

    def list_by_resume(
        self,
        *,
        resume_id: UUID,
    ) -> list[ResumeVersion]:
        result = self.session.execute(
            select(ResumeVersion)
            .where(
                ResumeVersion.resume_id == resume_id,
            )
            .order_by(
                ResumeVersion.version_number.desc(),
            )
        )

        return list(result.scalars().all())

    def get_latest(
        self,
        *,
        resume_id: UUID,
    ) -> ResumeVersion | None:
        result = self.session.execute(
            select(ResumeVersion)
            .where(
                ResumeVersion.resume_id == resume_id,
            )
            .order_by(
                ResumeVersion.version_number.desc(),
            )
            .limit(1)
        )

        return result.scalar_one_or_none()

    def get_next_version_number(
        self,
        *,
        resume_id: UUID,
    ) -> int:
        result = self.session.execute(
            select(
                func.coalesce(
                    func.max(ResumeVersion.version_number),
                    0,
                )
            ).where(
                ResumeVersion.resume_id == resume_id,
            )
        )

        latest_version_number = result.scalar_one()

        return latest_version_number + 1
