from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.certifications.models import Certification
from app.common.constants import (
    EmploymentType,
    ResumeVersionSource,
    SkillLevel,
)
from app.educations.models import Education
from app.experiences.models import Experience
from app.projects.models import Project
from app.resume_versions.service import ResumeVersionService
from app.resumes.exceptions import (
    ResumeAccessDenied,
    ResumeNotFound,
)
from app.resumes.models import Resume
from app.resumes.repository import ResumeRepository
from app.resumes.schemas import ImportResumeRequest
from app.skills.models import Skill


class ResumeService:
    """
    Business logic for resume management.
    """

    def __init__(
        self,
        repository: ResumeRepository,
        resume_version_service: ResumeVersionService,
        db: Session,
    ):
        self.repository = repository
        self.resume_version_service = resume_version_service
        self.db = db

    def create_resume(
        self,
        *,
        user_id: UUID,
        title: str,
        summary: str | None,
    ) -> Resume:
        resume = Resume(
            user_id=user_id,
            title=title,
            summary=summary,
        )

        resume = self.repository.create(resume)

        self.resume_version_service.create_version_from_resume(
            resume=resume,
            source=ResumeVersionSource.USER,
            change_summary="Resume created by user.",
        )

        self.db.commit()
        self.db.refresh(resume)

        return resume

    def import_resume(
        self,
        *,
        user_id: UUID,
        payload: ImportResumeRequest,
    ) -> Resume:
        """
        Import a complete resume and create its initial IMPORT version.

        The resume and all associated child records are persisted
        within the current database transaction.
        """

        resume = Resume(
            user_id=user_id,
            title=payload.title,
            summary=payload.summary,
        )

        for experience_data in payload.experiences:
            resume.experiences.append(
                Experience(
                    company=experience_data.company,
                    job_title=experience_data.job_title,
                    location=experience_data.location,
                    employment_type=experience_data.employment_type,
                    start_date=experience_data.start_date,
                    end_date=experience_data.end_date,
                    is_current=experience_data.is_current,
                    description=experience_data.description,
                    display_order=experience_data.display_order,
                )
            )

        for education_data in payload.educations:
            resume.educations.append(
                Education(
                    institution=education_data.institution,
                    degree=education_data.degree,
                    field_of_study=education_data.field_of_study,
                    location=education_data.location,
                    grade=education_data.grade,
                    start_date=education_data.start_date,
                    end_date=education_data.end_date,
                    is_current=education_data.is_current,
                    description=education_data.description,
                    display_order=education_data.display_order,
                )
            )

        for skill_data in payload.skills:
            resume.skills.append(
                Skill(
                    name=skill_data.name,
                    proficiency=skill_data.proficiency,
                    display_order=skill_data.display_order,
                )
            )

        for project_data in payload.projects:
            resume.projects.append(
                Project(
                    name=project_data.name,
                    description=project_data.description,
                    technologies=project_data.technologies,
                    project_url=(
                        str(project_data.project_url)
                        if project_data.project_url is not None
                        else None
                    ),
                    repository_url=(
                        str(project_data.repository_url)
                        if project_data.repository_url is not None
                        else None
                    ),
                    start_date=project_data.start_date,
                    end_date=project_data.end_date,
                    is_ongoing=project_data.is_ongoing,
                    display_order=project_data.display_order,
                )
            )

        for certification_data in payload.certifications:
            resume.certifications.append(
                Certification(
                    name=certification_data.name,
                    issuing_organization=(certification_data.issuing_organization),
                    credential_id=certification_data.credential_id,
                    credential_url=(
                        str(certification_data.credential_url)
                        if certification_data.credential_url is not None
                        else None
                    ),
                    issue_date=certification_data.issue_date,
                    expiration_date=certification_data.expiration_date,
                    does_not_expire=certification_data.does_not_expire,
                    display_order=certification_data.display_order,
                )
            )

        resume = self.repository.create_without_commit(
            resume,
        )

        self.resume_version_service.create_version_from_resume(
            resume=resume,
            source=ResumeVersionSource.IMPORT,
            change_summary="Resume imported by user.",
        )

        self.db.commit()
        self.db.refresh(resume)

        return resume

    def list_resumes(
        self,
        user_id: UUID,
    ) -> list[Resume]:
        return self.repository.list_by_user(user_id)

    def get_resume(
        self,
        *,
        user_id: UUID,
        resume_id: UUID,
    ) -> Resume:
        resume = self.repository.get_by_id(resume_id)

        if resume is None:
            raise ResumeNotFound("Resume not found.")

        if resume.user_id != user_id:
            raise ResumeAccessDenied(
                "You do not have permission to access this resume."
            )

        return resume

    def update_resume(
        self,
        *,
        user_id: UUID,
        resume_id: UUID,
        title: str,
        summary: str | None,
    ) -> Resume:
        resume = self.get_resume(
            user_id=user_id,
            resume_id=resume_id,
        )

        resume.title = title
        resume.summary = summary

        resume = self.repository.update(resume)

        self.resume_version_service.create_version_from_resume(
            resume=resume,
            source=ResumeVersionSource.USER,
            change_summary="Resume updated by user.",
        )

        self.db.commit()
        self.db.refresh(resume)

        return resume

    def restore_version(
        self,
        *,
        user_id: UUID,
        resume_id: UUID,
        version_id: UUID,
    ) -> Resume:
        """
        Restore a resume to the state captured by a historical version.

        The historical version remains immutable. The restored state is
        persisted as a new RESTORE version.
        """

        resume = self.get_resume(
            user_id=user_id,
            resume_id=resume_id,
        )

        resume = self.repository.get_for_restore(
            resume_id=resume.id,
        )

        if resume is None:
            raise ResumeNotFound("Resume not found.")

        version = self.resume_version_service.get_version_for_resume(
            resume_id=resume.id,
            version_id=version_id,
        )

        snapshot = version.snapshot

        resume.title = snapshot["title"]
        resume.summary = snapshot["summary"]
        resume.generated_content = snapshot["generated_content"]
        resume.generated_at = (
            datetime.fromisoformat(snapshot["generated_at"])
            if snapshot["generated_at"] is not None
            else None
        )
        resume.is_default = snapshot["is_default"]

        resume.experiences.clear()

        for experience_data in snapshot["experiences"]:
            resume.experiences.append(
                Experience(
                    company=experience_data["company"],
                    job_title=experience_data["job_title"],
                    location=experience_data["location"],
                    employment_type=EmploymentType(
                        experience_data["employment_type"],
                    ),
                    start_date=datetime.fromisoformat(
                        experience_data["start_date"],
                    ).date(),
                    end_date=(
                        datetime.fromisoformat(
                            experience_data["end_date"],
                        ).date()
                        if experience_data["end_date"] is not None
                        else None
                    ),
                    is_current=experience_data["is_current"],
                    description=experience_data["description"],
                    display_order=experience_data["display_order"],
                )
            )

        resume.educations.clear()

        for education_data in snapshot["educations"]:
            resume.educations.append(
                Education(
                    institution=education_data["institution"],
                    degree=education_data["degree"],
                    field_of_study=education_data["field_of_study"],
                    location=education_data["location"],
                    grade=education_data["grade"],
                    start_date=datetime.fromisoformat(
                        education_data["start_date"],
                    ).date(),
                    end_date=(
                        datetime.fromisoformat(
                            education_data["end_date"],
                        ).date()
                        if education_data["end_date"] is not None
                        else None
                    ),
                    is_current=education_data["is_current"],
                    description=education_data["description"],
                    display_order=education_data["display_order"],
                )
            )

        resume.skills.clear()

        for skill_data in snapshot["skills"]:
            resume.skills.append(
                Skill(
                    name=skill_data["name"],
                    proficiency=SkillLevel(
                        skill_data["proficiency"],
                    ),
                    display_order=skill_data["display_order"],
                )
            )

        resume.projects.clear()

        for project_data in snapshot["projects"]:
            resume.projects.append(
                Project(
                    name=project_data["name"],
                    description=project_data["description"],
                    technologies=project_data["technologies"],
                    project_url=project_data["project_url"],
                    repository_url=project_data["repository_url"],
                    start_date=(
                        datetime.fromisoformat(
                            project_data["start_date"],
                        ).date()
                        if project_data["start_date"] is not None
                        else None
                    ),
                    end_date=(
                        datetime.fromisoformat(
                            project_data["end_date"],
                        ).date()
                        if project_data["end_date"] is not None
                        else None
                    ),
                    is_ongoing=project_data["is_ongoing"],
                    display_order=project_data["display_order"],
                )
            )

        resume.certifications.clear()

        for certification_data in snapshot["certifications"]:
            resume.certifications.append(
                Certification(
                    name=certification_data["name"],
                    issuing_organization=(certification_data["issuing_organization"]),
                    credential_id=certification_data["credential_id"],
                    credential_url=certification_data["credential_url"],
                    issue_date=datetime.fromisoformat(
                        certification_data["issue_date"],
                    ).date(),
                    expiration_date=(
                        datetime.fromisoformat(
                            certification_data["expiration_date"],
                        ).date()
                        if certification_data["expiration_date"] is not None
                        else None
                    ),
                    does_not_expire=certification_data["does_not_expire"],
                    display_order=certification_data["display_order"],
                )
            )

        self.repository.update(resume)

        self.resume_version_service.create_version_from_resume(
            resume=resume,
            source=ResumeVersionSource.RESTORE,
            change_summary=(
                f"Resume restored from version " f"{version.version_number}."
            ),
        )

        self.db.commit()
        self.db.refresh(resume)

        return resume

    def delete_resume(
        self,
        *,
        user_id: UUID,
        resume_id: UUID,
    ) -> None:
        resume = self.get_resume(
            user_id=user_id,
            resume_id=resume_id,
        )

        self.repository.delete(resume)

        self.db.commit()
