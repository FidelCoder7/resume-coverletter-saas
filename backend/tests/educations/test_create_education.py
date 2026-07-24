from app.common.constants import ResumeVersionSource
from app.resume_versions.models import ResumeVersion
from tests.factories.resume_factory import create_resume
from tests.factories.user_factory import DEFAULT_PASSWORD, create_user


def test_create_education(client, db_session):
    user = create_user(
        db_session,
        email="john@example.com",
        password=DEFAULT_PASSWORD,
        verified=True,
    )

    resume = create_resume(
        db_session,
        user_id=user.id,
        title="Backend Resume",
        summary="Python Developer",
    )

    login = client.post(
        "/auth/login",
        data={
            "username": user.email,
            "password": DEFAULT_PASSWORD,
        },
    )

    token = login.json()["access_token"]

    response = client.post(
        f"/api/educations/resume/{resume.id}",
        json={
            "institution": "University of Nairobi",
            "degree": "Bachelor of Science",
            "field_of_study": "Computer Science",
            "location": "Nairobi",
            "grade": "First Class",
            "start_date": "2022-09-01",
            "end_date": None,
            "is_current": True,
            "description": "Relevant coursework and final year project.",
            "display_order": 0,
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["resume_id"] == str(resume.id)
    assert data["institution"] == "University of Nairobi"
    assert data["degree"] == "Bachelor of Science"
    assert data["field_of_study"] == "Computer Science"


## Authentication Test


def test_create_education_requires_authentication(client, db_session):
    user = create_user(
        db_session,
        verified=True,
    )

    resume = create_resume(
        db_session,
        user_id=user.id,
    )

    response = client.post(
        f"/api/educations/resume/{resume.id}",
        json={
            "institution": "University of Nairobi",
            "degree": "Bachelor of Science",
            "field_of_study": "Computer Science",
            "start_date": "2022-09-01",
            "is_current": True,
            "display_order": 0,
        },
    )

    assert response.status_code == 401


def test_create_education_creates_resume_version(
    client,
    db_session,
):
    user = create_user(
        db_session,
        email="version-create@example.com",
        password=DEFAULT_PASSWORD,
        verified=True,
    )

    resume = create_resume(
        db_session,
        user_id=user.id,
        title="Backend Resume",
        summary="Python Developer",
    )

    login = client.post(
        "/auth/login",
        data={
            "username": user.email,
            "password": DEFAULT_PASSWORD,
        },
    )

    token = login.json()["access_token"]

    response = client.post(
        f"/api/educations/resume/{resume.id}",
        json={
            "institution": "University of Nairobi",
            "degree": "Bachelor of Science",
            "field_of_study": "Computer Science",
            "location": "Nairobi",
            "grade": "First Class",
            "start_date": "2022-09-01",
            "end_date": None,
            "is_current": True,
            "description": "Relevant coursework and final year project.",
            "display_order": 0,
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 201

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
    assert version.change_summary == "Education added to resume."

    assert len(version.snapshot["educations"]) == 1

    education_snapshot = version.snapshot["educations"][0]

    assert education_snapshot["institution"] == "University of Nairobi"
    assert education_snapshot["degree"] == "Bachelor of Science"
    assert education_snapshot["field_of_study"] == "Computer Science"
    assert education_snapshot["location"] == "Nairobi"
    assert education_snapshot["grade"] == "First Class"
    assert education_snapshot["start_date"] == "2022-09-01"
    assert education_snapshot["end_date"] is None
    assert education_snapshot["is_current"] is True
    assert (
        education_snapshot["description"]
        == "Relevant coursework and final year project."
    )
    assert education_snapshot["display_order"] == 0
