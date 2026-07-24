from typing import Any

from app.resumes.models import Resume


class ResumeVersionSnapshotBuilder:
    """
    Builds a JSON-serializable snapshot of a resume's current state.

    The snapshot represents the complete persisted resume state at a
    particular point in time.
    """

    @staticmethod
    def build(
        resume: Resume,
    ) -> dict[str, Any]:
        return {
            "title": resume.title,
            "summary": resume.summary,
            "generated_content": resume.generated_content,
            "generated_at": (
                resume.generated_at.isoformat()
                if resume.generated_at is not None
                else None
            ),
            "is_default": resume.is_default,
            "experiences": [
                {
                    "company": experience.company,
                    "job_title": experience.job_title,
                    "location": experience.location,
                    "employment_type": experience.employment_type.value,
                    "start_date": experience.start_date.isoformat(),
                    "end_date": (
                        experience.end_date.isoformat()
                        if experience.end_date is not None
                        else None
                    ),
                    "is_current": experience.is_current,
                    "description": experience.description,
                    "display_order": experience.display_order,
                }
                for experience in resume.experiences
            ],
            "educations": [
                {
                    "institution": education.institution,
                    "degree": education.degree,
                    "field_of_study": education.field_of_study,
                    "location": education.location,
                    "grade": education.grade,
                    "start_date": education.start_date.isoformat(),
                    "end_date": (
                        education.end_date.isoformat()
                        if education.end_date is not None
                        else None
                    ),
                    "is_current": education.is_current,
                    "description": education.description,
                    "display_order": education.display_order,
                }
                for education in resume.educations
            ],
            "skills": [
                {
                    "name": skill.name,
                    "proficiency": skill.proficiency.value,
                    "display_order": skill.display_order,
                }
                for skill in resume.skills
            ],
            "projects": [
                {
                    "name": project.name,
                    "description": project.description,
                    "technologies": project.technologies,
                    "project_url": project.project_url,
                    "repository_url": project.repository_url,
                    "start_date": (
                        project.start_date.isoformat()
                        if project.start_date is not None
                        else None
                    ),
                    "end_date": (
                        project.end_date.isoformat()
                        if project.end_date is not None
                        else None
                    ),
                    "is_ongoing": project.is_ongoing,
                    "display_order": project.display_order,
                }
                for project in resume.projects
            ],
            "certifications": [
                {
                    "name": certification.name,
                    "issuing_organization": certification.issuing_organization,
                    "credential_id": certification.credential_id,
                    "credential_url": certification.credential_url,
                    "issue_date": certification.issue_date.isoformat(),
                    "expiration_date": (
                        certification.expiration_date.isoformat()
                        if certification.expiration_date is not None
                        else None
                    ),
                    "does_not_expire": certification.does_not_expire,
                    "display_order": certification.display_order,
                }
                for certification in resume.certifications
            ],
        }
