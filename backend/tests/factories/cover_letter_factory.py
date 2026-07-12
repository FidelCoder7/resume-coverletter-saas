from app.cover_letters.models import CoverLetter

DEFAULT_CONTENT = (
    "Dear Hiring Manager,\n\n"
    "I am excited to apply for this position because my experience in backend "
    "development, API design, and software engineering aligns well with your "
    "requirements. I enjoy building scalable applications using FastAPI, "
    "PostgreSQL, SQLAlchemy, and modern development practices.\n\n"
    "I would welcome the opportunity to discuss how I can contribute to your "
    "team. Thank you for your time and consideration.\n\n"
    "Sincerely,\n"
    "John Doe"
)


def make_cover_letter(
    *,
    resume_id,
    title: str = "Backend Developer Cover Letter",
    company_name: str = "Acme Inc.",
    job_title: str = "Backend Developer",
    content: str = DEFAULT_CONTENT,
) -> CoverLetter:
    return CoverLetter(
        resume_id=resume_id,
        title=title,
        company_name=company_name,
        job_title=job_title,
        content=content,
    )


def create_cover_letter(
    db,
    *,
    resume_id,
    **kwargs,
) -> CoverLetter:
    cover_letter = make_cover_letter(
        resume_id=resume_id,
        **kwargs,
    )

    db.add(cover_letter)
    db.commit()
    db.refresh(cover_letter)

    return cover_letter
