from datetime import date

from app.educations.models import Education


def make_education(
    *,
    resume_id,
    institution: str = "University of Nairobi",
    degree: str = "Bachelor of Science",
    field_of_study: str = "Computer Science",
    location: str = "Nairobi",
    grade: str | None = "First Class Honours",
    start_date: date = date(2020, 9, 1),
    end_date: date | None = None,
    is_current: bool = True,
    description: str = "Studied software engineering and computer science.",
    display_order: int = 0,
) -> Education:
    return Education(
        resume_id=resume_id,
        institution=institution,
        degree=degree,
        field_of_study=field_of_study,
        location=location,
        grade=grade,
        start_date=start_date,
        end_date=end_date,
        is_current=is_current,
        description=description,
        display_order=display_order,
    )


def create_education(
    db,
    *,
    resume_id,
    **kwargs,
) -> Education:
    education = make_education(
        resume_id=resume_id,
        **kwargs,
    )

    db.add(education)
    db.commit()
    db.refresh(education)

    return education
