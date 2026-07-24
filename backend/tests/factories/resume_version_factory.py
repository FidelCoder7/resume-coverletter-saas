from typing import Any

from app.common.constants import ResumeVersionSource
from app.resume_versions.models import ResumeVersion


def make_resume_version(
    *,
    resume_id,
    version_number: int = 1,
    snapshot: dict[str, Any] | None = None,
    change_summary: str | None = None,
    source: ResumeVersionSource = ResumeVersionSource.USER,
) -> ResumeVersion:
    return ResumeVersion(
        resume_id=resume_id,
        version_number=version_number,
        snapshot=snapshot
        or {
            "title": "Backend Resume",
            "summary": "Python Backend Developer",
        },
        change_summary=change_summary,
        source=source,
    )


def create_resume_version(
    db,
    *,
    resume_id,
    version_number: int = 1,
    snapshot: dict[str, Any] | None = None,
    change_summary: str | None = None,
    source: ResumeVersionSource = ResumeVersionSource.USER,
) -> ResumeVersion:
    version = make_resume_version(
        resume_id=resume_id,
        version_number=version_number,
        snapshot=snapshot,
        change_summary=change_summary,
        source=source,
    )

    db.add(version)
    db.commit()
    db.refresh(version)

    return version
