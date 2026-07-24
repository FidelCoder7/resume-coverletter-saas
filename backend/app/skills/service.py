from uuid import UUID

from app.common.constants import ResumeVersionSource, SkillLevel
from app.resume_versions.service import ResumeVersionService
from app.resumes.repository import ResumeRepository
from app.skills.exceptions import (
    SkillAccessDenied,
    SkillNotFound,
)
from app.skills.models import Skill
from app.skills.repository import SkillRepository


class SkillService:
    """
    Business logic for resume skill management.
    """

    def __init__(
        self,
        repository: SkillRepository,
        resume_repository: ResumeRepository,
        resume_version_service: ResumeVersionService,
    ) -> None:
        self.repository = repository
        self.resume_repository = resume_repository
        self.resume_version_service = resume_version_service

    def _verify_resume_owner(
        self,
        *,
        resume_id: UUID,
        user_id: UUID,
    ):
        """
        Ensure the resume belongs to the authenticated user.
        """

        resume = self.resume_repository.get_by_id(
            resume_id,
        )

        if resume is None:
            raise SkillNotFound(
                "Resume not found.",
            )

        if resume.user_id != user_id:
            raise SkillAccessDenied(
                "You do not have permission to access this resume.",
            )

        return resume

    def create_skill(
        self,
        *,
        user_id: UUID,
        resume_id: UUID,
        name: str,
        proficiency: SkillLevel,
        display_order: int,
    ) -> Skill:
        resume = self._verify_resume_owner(
            resume_id=resume_id,
            user_id=user_id,
        )

        skill = Skill(
            resume_id=resume_id,
            name=name,
            proficiency=proficiency,
            display_order=display_order,
        )

        skill = self.repository.create(
            skill,
        )

        self.resume_version_service.create_version_from_resume(
            resume=resume,
            source=ResumeVersionSource.USER,
            change_summary="Skill added to resume.",
        )

        self.repository.db.commit()
        self.repository.db.refresh(skill)

        return skill

    def list_skills(
        self,
        *,
        user_id: UUID,
        resume_id: UUID,
    ) -> list[Skill]:
        self._verify_resume_owner(
            resume_id=resume_id,
            user_id=user_id,
        )

        return self.repository.list_by_resume(
            resume_id,
        )

    def get_skill(
        self,
        *,
        user_id: UUID,
        skill_id: UUID,
    ) -> Skill:
        skill = self.repository.get_by_id(
            skill_id,
        )

        if skill is None:
            raise SkillNotFound(
                "Skill not found.",
            )

        self._verify_resume_owner(
            resume_id=skill.resume_id,
            user_id=user_id,
        )

        return skill

    def update_skill(
        self,
        *,
        user_id: UUID,
        skill_id: UUID,
        name: str,
        proficiency: SkillLevel,
        display_order: int,
    ) -> Skill:
        skill = self.get_skill(
            user_id=user_id,
            skill_id=skill_id,
        )

        skill.name = name
        skill.proficiency = proficiency
        skill.display_order = display_order

        skill = self.repository.update(
            skill,
        )

        resume = self._verify_resume_owner(
            resume_id=skill.resume_id,
            user_id=user_id,
        )

        self.resume_version_service.create_version_from_resume(
            resume=resume,
            source=ResumeVersionSource.USER,
            change_summary="Skill updated on resume.",
        )

        self.repository.db.commit()
        self.repository.db.refresh(skill)

        return skill

    def delete_skill(
        self,
        *,
        user_id: UUID,
        skill_id: UUID,
    ) -> None:
        skill = self.get_skill(
            user_id=user_id,
            skill_id=skill_id,
        )

        resume = self._verify_resume_owner(
            resume_id=skill.resume_id,
            user_id=user_id,
        )

        self.repository.delete(
            skill,
        )

        self.resume_version_service.create_version_from_resume(
            resume=resume,
            source=ResumeVersionSource.USER,
            change_summary="Skill removed from resume.",
        )

        self.repository.db.commit()
