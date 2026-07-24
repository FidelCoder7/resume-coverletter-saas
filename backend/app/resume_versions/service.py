from typing import Any
from uuid import UUID

from app.common.constants import ResumeVersionSource
from app.resume_versions.exceptions import ResumeVersionNotFound
from app.resume_versions.models import ResumeVersion
from app.resume_versions.repository import ResumeVersionRepository
from app.resume_versions.snapshot import ResumeVersionSnapshotBuilder
from app.resumes.models import Resume


class ResumeVersionService:
    """
    Business logic for resume version history.
    """

    def __init__(
        self,
        repository: ResumeVersionRepository,
    ) -> None:
        self.repository = repository

    def create_version(
        self,
        *,
        resume_id: UUID,
        snapshot: dict[str, Any],
        source: ResumeVersionSource,
        change_summary: str | None = None,
    ) -> ResumeVersion:
        """
        Create a version using an explicitly supplied snapshot.

        The supplied snapshot is persisted exactly as provided.

        This method flushes the new version into the current transaction.
        It does not commit.
        """

        version_number = self.repository.get_next_version_number(
            resume_id=resume_id,
        )

        return self.repository.create(
            resume_id=resume_id,
            version_number=version_number,
            snapshot=snapshot,
            source=source,
            change_summary=change_summary,
        )

    def create_version_from_resume(
        self,
        *,
        resume: Resume,
        source: ResumeVersionSource,
        change_summary: str | None = None,
    ) -> ResumeVersion:
        """
        Create a version by snapshotting the current resume state.

        The version is flushed into the current transaction but is not
        committed here.
        """

        snapshot = ResumeVersionSnapshotBuilder.build(
            resume,
        )

        return self.create_version(
            resume_id=resume.id,
            snapshot=snapshot,
            source=source,
            change_summary=change_summary,
        )

    def get_version(
        self,
        *,
        version_id: UUID,
    ) -> ResumeVersion | None:
        return self.repository.get_by_id(
            version_id=version_id,
        )

    def get_version_for_resume(
        self,
        *,
        resume_id: UUID,
        version_id: UUID,
    ) -> ResumeVersion:
        """
        Retrieve a version only when it belongs to the requested resume.

        Raises:
            ResumeVersionNotFound:
                If the version does not exist or belongs to another resume.
        """

        version = self.repository.get_by_resume_and_id(
            resume_id=resume_id,
            version_id=version_id,
        )

        if version is None:
            raise ResumeVersionNotFound(
                "Resume version not found.",
            )

        return version

    def get_version_history(
        self,
        *,
        resume_id: UUID,
    ) -> list[ResumeVersion]:
        return self.repository.list_by_resume(
            resume_id=resume_id,
        )

    def get_latest_version(
        self,
        *,
        resume_id: UUID,
    ) -> ResumeVersion | None:
        return self.repository.get_latest(
            resume_id=resume_id,
        )
