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
