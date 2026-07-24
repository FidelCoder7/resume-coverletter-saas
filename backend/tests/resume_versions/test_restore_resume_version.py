from uuid import uuid4

from sqlalchemy import select

from app.certifications.models import Certification
from app.common.constants import ResumeVersionSource
from app.educations.models import Education
from app.experiences.models import Experience
from app.projects.models import Project
from app.resume_versions.repository import ResumeVersionRepository
from app.resume_versions.service import ResumeVersionService
from app.skills.models import Skill
from tests.factories.certification_factory import create_certification
from tests.factories.education_factory import create_education
from tests.factories.experience_factory import create_experience
from tests.factories.project_factory import create_project
from tests.factories.resume_factory import create_resume
from tests.factories.skill_factory import create_skill
from tests.utils import auth_headers, authenticated_user


def test_restore_resume_version(
    client,
    db_session,
):
    _, token = authenticated_user(
        client,
        db_session,
    )

    created = client.post(
        "/api/resumes",
        json={
            "title": "Original Resume",
            "summary": "Original summary.",
        },
        headers=auth_headers(token),
    )

    assert created.status_code == 201

    resume_id = created.json()["id"]

    versions = client.get(
        f"/api/resumes/{resume_id}/versions",
        headers=auth_headers(token),
    )

    assert versions.status_code == 200
    assert len(versions.json()) == 1

    original_version = versions.json()[0]

    assert original_version["version_number"] == 1
    assert original_version["source"] == "user"
    assert original_version["snapshot"]["title"] == "Original Resume"
    assert original_version["snapshot"]["summary"] == "Original summary."

    updated = client.put(
        f"/api/resumes/{resume_id}",
        json={
            "title": "Updated Resume",
            "summary": "Updated summary.",
        },
        headers=auth_headers(token),
    )

    assert updated.status_code == 200

    restored = client.post(
        (f"/api/resumes/{resume_id}/versions/" f"{original_version['id']}/restore"),
        headers=auth_headers(token),
    )

    assert restored.status_code == 200

    data = restored.json()

    assert data["id"] == resume_id
    assert data["title"] == "Original Resume"
    assert data["summary"] == "Original summary."

    versions = client.get(
        f"/api/resumes/{resume_id}/versions",
        headers=auth_headers(token),
    )

    assert versions.status_code == 200

    history = versions.json()

    assert len(history) == 3

    assert history[0]["version_number"] == 3
    assert history[0]["source"] == "restore"
    assert history[0]["change_summary"] == ("Resume restored from version 1.")

    assert history[1]["version_number"] == 2
    assert history[1]["source"] == "user"

    assert history[2]["version_number"] == 1
    assert history[2]["source"] == "user"

    assert history[2]["snapshot"]["title"] == "Original Resume"
    assert history[2]["snapshot"]["summary"] == "Original summary."


def test_restore_version_restores_all_nested_resume_content(
    client,
    db_session,
):
    user, token = authenticated_user(
        client,
        db_session,
    )

    resume = create_resume(
        db_session,
        user_id=user.id,
        title="Full Resume",
        summary="Complete resume.",
    )

    experience = create_experience(
        db_session,
        resume_id=resume.id,
    )

    education = create_education(
        db_session,
        resume_id=resume.id,
    )

    skill = create_skill(
        db_session,
        resume_id=resume.id,
    )

    project = create_project(
        db_session,
        resume_id=resume.id,
    )

    certification = create_certification(
        db_session,
        resume_id=resume.id,
    )

    db_session.commit()

    # Create the historical version directly through the service layer.
    # There is intentionally no public POST /versions endpoint.
    version_service = ResumeVersionService(
        repository=ResumeVersionRepository(db_session),
    )

    version = version_service.create_version_from_resume(
        resume=resume,
        source=ResumeVersionSource.USER,
        change_summary="Initial complete resume snapshot.",
    )

    db_session.commit()

    version_id = version.id

    # Preserve the original nested content values before deleting the
    # records. Restore creates new nested records from the snapshot, so
    # their IDs are not expected to match the original records.
    original_experience = {
        "company": experience.company,
        "job_title": experience.job_title,
        "location": experience.location,
        "employment_type": experience.employment_type,
        "start_date": experience.start_date,
        "end_date": experience.end_date,
        "is_current": experience.is_current,
        "description": experience.description,
        "display_order": experience.display_order,
    }

    original_education = {
        "institution": education.institution,
        "degree": education.degree,
        "field_of_study": education.field_of_study,
        "location": education.location,
        "grade": education.grade,
        "start_date": education.start_date,
        "end_date": education.end_date,
        "is_current": education.is_current,
        "description": education.description,
        "display_order": education.display_order,
    }

    original_skill = {
        "name": skill.name,
        "proficiency": skill.proficiency,
        "display_order": skill.display_order,
    }

    original_project = {
        "name": project.name,
        "description": project.description,
        "technologies": project.technologies,
        "project_url": project.project_url,
        "repository_url": project.repository_url,
        "start_date": project.start_date,
        "end_date": project.end_date,
        "is_ongoing": project.is_ongoing,
        "display_order": project.display_order,
    }

    original_certification = {
        "name": certification.name,
        "issuing_organization": certification.issuing_organization,
        "credential_id": certification.credential_id,
        "credential_url": certification.credential_url,
        "issue_date": certification.issue_date,
        "expiration_date": certification.expiration_date,
        "does_not_expire": certification.does_not_expire,
        "display_order": certification.display_order,
    }

    # Change the resume by deleting all nested records.
    db_session.delete(experience)
    db_session.delete(education)
    db_session.delete(skill)
    db_session.delete(project)
    db_session.delete(certification)

    resume.title = "Modified Resume"
    resume.summary = "Modified summary."

    db_session.commit()

    restored = client.post(
        f"/api/resumes/{resume.id}/versions/{version_id}/restore",
        headers=auth_headers(token),
    )

    assert restored.status_code == 200

    data = restored.json()

    assert data["title"] == "Full Resume"
    assert data["summary"] == "Complete resume."

    # The restore workflow recreates nested records from the historical
    # snapshot. Verify the restored content directly in the database.
    restored_experiences = list(
        db_session.scalars(
            select(Experience).where(
                Experience.resume_id == resume.id,
            )
        )
    )

    assert len(restored_experiences) == 1

    restored_experience = restored_experiences[0]

    assert restored_experience.company == (original_experience["company"])
    assert restored_experience.job_title == (original_experience["job_title"])
    assert restored_experience.location == (original_experience["location"])
    assert restored_experience.employment_type == (
        original_experience["employment_type"]
    )
    assert restored_experience.start_date == (original_experience["start_date"])
    assert restored_experience.end_date == (original_experience["end_date"])
    assert restored_experience.is_current == (original_experience["is_current"])
    assert restored_experience.description == (original_experience["description"])
    assert restored_experience.display_order == (original_experience["display_order"])

    restored_educations = list(
        db_session.scalars(
            select(Education).where(
                Education.resume_id == resume.id,
            )
        )
    )

    assert len(restored_educations) == 1

    restored_education = restored_educations[0]

    assert restored_education.institution == (original_education["institution"])
    assert restored_education.degree == (original_education["degree"])
    assert restored_education.field_of_study == (original_education["field_of_study"])
    assert restored_education.location == (original_education["location"])
    assert restored_education.grade == (original_education["grade"])
    assert restored_education.start_date == (original_education["start_date"])
    assert restored_education.end_date == (original_education["end_date"])
    assert restored_education.is_current == (original_education["is_current"])
    assert restored_education.description == (original_education["description"])
    assert restored_education.display_order == (original_education["display_order"])

    restored_skills = list(
        db_session.scalars(
            select(Skill).where(
                Skill.resume_id == resume.id,
            )
        )
    )

    assert len(restored_skills) == 1

    restored_skill = restored_skills[0]

    assert restored_skill.name == original_skill["name"]
    assert restored_skill.proficiency == (original_skill["proficiency"])
    assert restored_skill.display_order == (original_skill["display_order"])

    restored_projects = list(
        db_session.scalars(
            select(Project).where(
                Project.resume_id == resume.id,
            )
        )
    )

    assert len(restored_projects) == 1

    restored_project = restored_projects[0]

    assert restored_project.name == original_project["name"]
    assert restored_project.description == (original_project["description"])
    assert restored_project.technologies == (original_project["technologies"])
    assert restored_project.project_url == (original_project["project_url"])
    assert restored_project.repository_url == (original_project["repository_url"])
    assert restored_project.start_date == (original_project["start_date"])
    assert restored_project.end_date == (original_project["end_date"])
    assert restored_project.is_ongoing == (original_project["is_ongoing"])
    assert restored_project.display_order == (original_project["display_order"])

    restored_certifications = list(
        db_session.scalars(
            select(Certification).where(
                Certification.resume_id == resume.id,
            )
        )
    )

    assert len(restored_certifications) == 1

    restored_certification = restored_certifications[0]

    assert restored_certification.name == (original_certification["name"])
    assert restored_certification.issuing_organization == (
        original_certification["issuing_organization"]
    )
    assert restored_certification.credential_id == (
        original_certification["credential_id"]
    )
    assert restored_certification.credential_url == (
        original_certification["credential_url"]
    )
    assert restored_certification.issue_date == (original_certification["issue_date"])
    assert restored_certification.expiration_date == (
        original_certification["expiration_date"]
    )
    assert restored_certification.does_not_expire == (
        original_certification["does_not_expire"]
    )
    assert restored_certification.display_order == (
        original_certification["display_order"]
    )


def test_restore_resume_version_requires_ownership(
    client,
    db_session,
):
    _, owner_token = authenticated_user(
        client,
        db_session,
    )

    created = client.post(
        "/api/resumes",
        json={
            "title": "Owner Resume",
            "summary": "Private resume.",
        },
        headers=auth_headers(owner_token),
    )

    assert created.status_code == 201

    resume_id = created.json()["id"]

    versions = client.get(
        f"/api/resumes/{resume_id}/versions",
        headers=auth_headers(owner_token),
    )

    assert versions.status_code == 200

    version_id = versions.json()[0]["id"]

    _, attacker_token = authenticated_user(
        client,
        db_session,
    )

    response = client.post(
        f"/api/resumes/{resume_id}/versions/{version_id}/restore",
        headers=auth_headers(attacker_token),
    )

    assert response.status_code == 404


def test_restore_unknown_version_returns_404(
    client,
    db_session,
):
    _, token = authenticated_user(
        client,
        db_session,
    )

    created = client.post(
        "/api/resumes",
        json={
            "title": "Resume",
            "summary": "Summary.",
        },
        headers=auth_headers(token),
    )

    assert created.status_code == 201

    resume_id = created.json()["id"]

    response = client.post(
        f"/api/resumes/{resume_id}/versions/{uuid4()}/restore",
        headers=auth_headers(token),
    )

    assert response.status_code == 404
