from app.common.constants import ResumeVersionSource
from app.resume_versions.models import ResumeVersion
from tests.factories.experience_factory import create_experience
from tests.factories.resume_factory import create_resume
from tests.factories.user_factory import (
    DEFAULT_PASSWORD,
    create_user,
)


def test_update_experience(client, db_session):
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

    experience = create_experience(
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
        f"/api/experiences/{experience.id}",
        json={
            "company": "Microsoft",
            "job_title": "Senior Software Engineer",
            "location": "Nairobi",
            "employment_type": "full_time",
            "start_date": "2023-01-01",
            "end_date": None,
            "is_current": True,
            "description": "Led backend development.",
            "display_order": 1,
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["company"] == "Microsoft"
    assert data["job_title"] == "Senior Software Engineer"
    assert data["location"] == "Nairobi"
    assert data["display_order"] == 1


def test_cannot_update_another_users_experience(
    client,
    db_session,
):
    owner = create_user(
        db_session,
        verified=True,
    )

    other_user = create_user(
        db_session,
        verified=True,
    )

    resume = create_resume(
        db_session,
        user_id=owner.id,
    )

    experience = create_experience(
        db_session,
        resume_id=resume.id,
    )

    login = client.post(
        "/auth/login",
        data={
            "username": other_user.email,
            "password": DEFAULT_PASSWORD,
        },
    )

    token = login.json()["access_token"]

    response = client.put(
        f"/api/experiences/{experience.id}",
        json={
            "company": "Google",
            "job_title": "Engineer",
            "location": "Remote",
            "employment_type": "full_time",
            "start_date": "2023-01-01",
            "end_date": None,
            "is_current": True,
            "description": "Should not update.",
            "display_order": 0,
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 403


def test_update_unknown_experience_returns_404(
    client,
    db_session,
):
    from uuid import uuid4

    user = create_user(
        db_session,
        verified=True,
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
        f"/api/experiences/{uuid4()}",
        json={
            "company": "Google",
            "job_title": "Engineer",
            "location": "Remote",
            "employment_type": "full_time",
            "start_date": "2023-01-01",
            "end_date": None,
            "is_current": True,
            "description": "Unknown experience.",
            "display_order": 0,
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 404


def test_update_experience_creates_resume_version(
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

    experience = create_experience(
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
        f"/api/experiences/{experience.id}",
        json={
            "company": "Microsoft",
            "job_title": "Senior Software Engineer",
            "location": "Nairobi",
            "employment_type": "full_time",
            "start_date": "2023-01-01",
            "end_date": None,
            "is_current": True,
            "description": "Led backend development.",
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
    assert version.change_summary == "Experience updated by user."

    assert len(version.snapshot["experiences"]) == 1

    experience_snapshot = version.snapshot["experiences"][0]

    assert experience_snapshot["company"] == "Microsoft"
    assert experience_snapshot["job_title"] == "Senior Software Engineer"
    assert experience_snapshot["location"] == "Nairobi"
    assert experience_snapshot["description"] == "Led backend development."
    assert experience_snapshot["display_order"] == 1
