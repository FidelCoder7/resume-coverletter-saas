from app.common.constants import ResumeVersionSource
from app.resume_versions.models import ResumeVersion
from tests.factories.education_factory import create_education
from tests.factories.resume_factory import create_resume
from tests.factories.user_factory import (
    DEFAULT_PASSWORD,
    create_user,
)


def test_update_education(
    client,
    db_session,
):
    user = create_user(
        db_session,
        email="john@example.com",
        password=DEFAULT_PASSWORD,
        verified=True,
    )

    resume = create_resume(
        db_session,
        user_id=user.id,
    )

    education = create_education(
        db_session,
        resume_id=resume.id,
    )

    login = client.post(
        "/auth/login",
        data={
            "username": user.email,
            "password": DEFAULT_PASSWORD,
        },
    )

    token = login.json()["access_token"]

    response = client.put(
        f"/api/educations/{education.id}",
        json={
            "institution": "Stanford University",
            "degree": "Master of Science",
            "field_of_study": "Artificial Intelligence",
            "location": "California",
            "grade": "4.0 GPA",
            "start_date": "2021-09-01",
            "end_date": "2023-06-30",
            "is_current": False,
            "description": "Focused on machine learning.",
            "display_order": 1,
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["institution"] == "Stanford University"
    assert data["degree"] == "Master of Science"
    assert data["field_of_study"] == "Artificial Intelligence"
    assert data["location"] == "California"
    assert data["grade"] == "4.0 GPA"
    assert data["display_order"] == 1


def test_update_education_requires_authentication(
    client,
    db_session,
):
    user = create_user(
        db_session,
        verified=True,
    )

    resume = create_resume(
        db_session,
        user_id=user.id,
    )

    education = create_education(
        db_session,
        resume_id=resume.id,
    )

    response = client.put(
        f"/api/educations/{education.id}",
        json={
            "institution": "Updated University",
            "degree": "Updated Degree",
            "field_of_study": "Updated Field",
            "location": "Updated Location",
            "grade": "Updated Grade",
            "start_date": "2021-01-01",
            "end_date": "2023-01-01",
            "is_current": False,
            "description": "Updated description.",
            "display_order": 0,
        },
    )

    assert response.status_code == 401


def test_update_education_creates_resume_version(
    client,
    db_session,
):
    user = create_user(
        db_session,
        email="version-update@example.com",
        password=DEFAULT_PASSWORD,
        verified=True,
    )

    resume = create_resume(
        db_session,
        user_id=user.id,
    )

    education = create_education(
        db_session,
        resume_id=resume.id,
    )

    login = client.post(
        "/auth/login",
        data={
            "username": user.email,
            "password": DEFAULT_PASSWORD,
        },
    )

    token = login.json()["access_token"]

    response = client.put(
        f"/api/educations/{education.id}",
        json={
            "institution": "Stanford University",
            "degree": "Master of Science",
            "field_of_study": "Artificial Intelligence",
            "location": "California",
            "grade": "4.0 GPA",
            "start_date": "2021-09-01",
            "end_date": "2023-06-30",
            "is_current": False,
            "description": "Focused on machine learning.",
            "display_order": 1,
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    db_session.expire_all()

    versions = (
        db_session.query(ResumeVersion)
        .filter(
            ResumeVersion.resume_id == resume.id,
        )
        .order_by(
            ResumeVersion.version_number.asc(),
        )
        .all()
    )

    assert len(versions) == 1

    version = versions[0]

    assert version.version_number == 1
    assert version.source == ResumeVersionSource.USER
    assert version.change_summary == "Education updated on resume."

    assert len(version.snapshot["educations"]) == 1

    education_snapshot = version.snapshot["educations"][0]

    assert education_snapshot["institution"] == "Stanford University"
    assert education_snapshot["degree"] == "Master of Science"
    assert education_snapshot["field_of_study"] == "Artificial Intelligence"
    assert education_snapshot["location"] == "California"
    assert education_snapshot["grade"] == "4.0 GPA"
    assert education_snapshot["start_date"] == "2021-09-01"
    assert education_snapshot["end_date"] == "2023-06-30"
    assert education_snapshot["is_current"] is False
    assert education_snapshot["description"] == "Focused on machine learning."
    assert education_snapshot["display_order"] == 1
