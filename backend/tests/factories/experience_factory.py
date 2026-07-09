from datetime import date

from app.common.constants import EmploymentType
from app.experiences.models import Experience


def make_experience(
    *,
    resume_id,
    company: str = "OpenAI",
    job_title: str = "Software Engineer",
    location: str = "Remote",
    employment_type: EmploymentType = EmploymentType.FULL_TIME,
    start_date: date = date(2024, 1, 1),
    end_date: date | None = None,
    is_current: bool = True,
    description: str = "Built scalable backend APIs.",
    display_order: int = 0,
) -> Experience:
    return Experience(
        resume_id=resume_id,
        company=company,
        job_title=job_title,
        location=location,
        employment_type=employment_type,
        start_date=start_date,
        end_date=end_date,
        is_current=is_current,
        description=description,
        display_order=display_order,
    )


def create_experience(
    db,
    *,
    resume_id,
    **kwargs,
) -> Experience:
    experience = make_experience(
        resume_id=resume_id,
        **kwargs,
    )

    db.add(experience)
    db.commit()
    db.refresh(experience)

    return experience
