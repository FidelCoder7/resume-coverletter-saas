from app.common.constants import SkillLevel
from app.skills.models import Skill


def make_skill(
    *,
    resume_id,
    name: str = "Python",
    proficiency: SkillLevel = SkillLevel.ADVANCED,
    display_order: int = 0,
) -> Skill:
    return Skill(
        resume_id=resume_id,
        name=name,
        proficiency=proficiency,
        display_order=display_order,
    )


def create_skill(
    db,
    *,
    resume_id,
    **kwargs,
) -> Skill:
    skill = make_skill(
        resume_id=resume_id,
        **kwargs,
    )

    db.add(skill)
    db.commit()
    db.refresh(skill)

    return skill
