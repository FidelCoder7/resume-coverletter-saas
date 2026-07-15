from datetime import datetime

from app.resumes.models import Resume


def make_resume(
    *,
    user_id,
    title: str = "Backend Resume",
    summary: str = "Python Backend Developer",
    generated_content: str | None = None,
    generated_at: datetime | None = None,
    is_default: bool = False,
) -> Resume:
    return Resume(
        user_id=user_id,
        title=title,
        summary=summary,
        generated_content=generated_content,
        generated_at=generated_at,
        is_default=is_default,
    )


def create_resume(
    db,
    *,
    user_id,
    **kwargs,
) -> Resume:
    resume = make_resume(
        user_id=user_id,
        **kwargs,
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    return resume
