from datetime import date

from app.projects.models import Project


def make_project(
    *,
    resume_id,
    name: str = "AI Resume Builder",
    description: str = (
        "A full-stack SaaS application for creating AI-powered resumes."
    ),
    technologies: str = "FastAPI, PostgreSQL, Docker",
    project_url: str | None = "https://example.com/",
    repository_url: str | None = ("https://github.com/example/ai-resume-builder"),
    start_date: date | None = date(2025, 1, 1),
    end_date: date | None = None,
    is_ongoing: bool = True,
    display_order: int = 0,
) -> Project:
    return Project(
        resume_id=resume_id,
        name=name,
        description=description,
        technologies=technologies,
        project_url=project_url,
        repository_url=repository_url,
        start_date=start_date,
        end_date=end_date,
        is_ongoing=is_ongoing,
        display_order=display_order,
    )


def create_project(
    db,
    *,
    resume_id,
    **kwargs,
) -> Project:
    project = make_project(
        resume_id=resume_id,
        **kwargs,
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project
