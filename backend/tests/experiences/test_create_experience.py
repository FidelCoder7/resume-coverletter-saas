from app.common.constants import ResumeVersionSource
from app.resume_versions.models import ResumeVersion
from app.resumes.models import Resume
from tests.factories.user_factory import DEFAULT_PASSWORD, create_user


def test_create_experience(client, db_session):
    user = create_user(
        db_session,
        email="john@example.com",
        password=DEFAULT_PASSWORD,
        verified=True,
    )

    resume = Resume(
        user_id=user.id,
        title="Backend Resume",
        summary="Python Developer",
    )

    db_session.add(resume)
    db_session.commit()
    db_session.refresh(resume)

    login = client.post(
        "/auth/login",
        data={
            "username": user.email,
            "password": DEFAULT_PASSWORD,
        },
    )

    token = login.json()["access_token"]

    response = client.post(
        f"/api/experiences/resume/{resume.id}",
        json={
            "company": "OpenAI",
            "job_title": "Software Engineer",
            "location": "Remote",
            "employment_type": "full_time",
            "start_date": "2024-01-01",
            "end_date": None,
            "is_current": True,
            "description": "Built AI APIs.",
            "display_order": 0,
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["company"] == "OpenAI"
    assert data["job_title"] == "Software Engineer"
    assert data["resume_id"] == str(resume.id)


def test_create_experience_requires_authentication(client, db_session):
    user = create_user(
        db_session,
        verified=True,
    )

    resume = Resume(
        user_id=user.id,
        title="Resume",
    )

    db_session.add(resume)
    db_session.commit()
    db_session.refresh(resume)

    response = client.post(
        f"/api/experiences/resume/{resume.id}",
        json={
            "company": "OpenAI",
            "job_title": "Engineer",
            "employment_type": "full_time",
            "start_date": "2024-01-01",
            "is_current": True,
            "display_order": 0,
        },
    )

    assert response.status_code == 401


def test_create_experience_creates_resume_version(
    client,
    db_session,
):
    user = create_user(
        db_session,
        email="version-create@example.com",
        password=DEFAULT_PASSWORD,
        verified=True,
    )

    resume = Resume(
        user_id=user.id,
        title="Backend Resume",
        summary="Python Developer",
    )

    db_session.add(resume)
    db_session.commit()
    db_session.refresh(resume)

    login = client.post(
        "/auth/login",
        data={
            "username": user.email,
            "password": DEFAULT_PASSWORD,
        },
    )

    token = login.json()["access_token"]

    response = client.post(
        f"/api/experiences/resume/{resume.id}",
        json={
            "company": "OpenAI",
            "job_title": "Software Engineer",
            "location": "Remote",
            "employment_type": "full_time",
            "start_date": "2024-01-01",
            "end_date": None,
            "is_current": True,
            "description": "Built AI APIs.",
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
    assert version.change_summary == "Experience added to resume."

    assert len(version.snapshot["experiences"]) == 1

    experience_snapshot = version.snapshot["experiences"][0]

    assert experience_snapshot["company"] == "OpenAI"
    assert experience_snapshot["job_title"] == "Software Engineer"
    assert experience_snapshot["location"] == "Remote"
    assert experience_snapshot["employment_type"] == "full_time"
    assert experience_snapshot["start_date"] == "2024-01-01"
    assert experience_snapshot["end_date"] is None
    assert experience_snapshot["is_current"] is True
    assert experience_snapshot["description"] == "Built AI APIs."
    assert experience_snapshot["display_order"] == 0
