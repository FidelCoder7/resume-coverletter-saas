from app.resumes.models import Resume


def make_resume(
    *,
    user_id,
    title: str = "Backend Resume",
    summary: str = "Python Backend Developer",
    is_default: bool = False,
) -> Resume:
    return Resume(
        user_id=user_id,
        title=title,
        summary=summary,
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
