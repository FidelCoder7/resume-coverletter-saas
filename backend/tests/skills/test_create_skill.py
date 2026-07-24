from app.common.constants import ResumeVersionSource
from app.resume_versions.models import ResumeVersion
from app.resumes.models import Resume
from tests.factories.user_factory import DEFAULT_PASSWORD, create_user


def test_create_skill(client, db_session):
    user = create_user(
        db_session,
        email="john@example.com",
        password=DEFAULT_PASSWORD,
        verified=True,
    )

    resume = Resume(
        user_id=user.id,
        title="Backend Resume",
        summary="Python Backend Developer",
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

    assert login.status_code == 200

    token = login.json()["access_token"]

    response = client.post(
        f"/api/skills/resume/{resume.id}",
        json={
            "name": "Python",
            "proficiency": "advanced",
            "display_order": 0,
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Python"
    assert data["proficiency"] == "advanced"
    assert data["resume_id"] == str(resume.id)
    assert data["display_order"] == 0


def test_create_skill_requires_authentication(client, db_session):
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
        f"/api/skills/resume/{resume.id}",
        json={
            "name": "Python",
            "proficiency": "advanced",
            "display_order": 0,
        },
    )

    assert response.status_code == 401


def test_create_skill_creates_resume_version(
    client,
    db_session,
):
    user = create_user(
        db_session,
        email="version-create-skill@example.com",
        password=DEFAULT_PASSWORD,
        verified=True,
    )

    resume = Resume(
        user_id=user.id,
        title="Backend Resume",
        summary="Python Backend Developer",
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

    assert login.status_code == 200

    token = login.json()["access_token"]

    response = client.post(
        f"/api/skills/resume/{resume.id}",
        json={
            "name": "Python",
            "proficiency": "advanced",
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
    assert version.change_summary == "Skill added to resume."

    assert len(version.snapshot["skills"]) == 1

    skill_snapshot = version.snapshot["skills"][0]

    assert skill_snapshot["name"] == "Python"
    assert skill_snapshot["proficiency"] == "advanced"
    assert skill_snapshot["display_order"] == 0
