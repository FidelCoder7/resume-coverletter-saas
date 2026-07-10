from tests.factories.resume_factory import create_resume
from tests.factories.skill_factory import create_skill
from tests.factories.user_factory import (
    DEFAULT_PASSWORD,
    create_user,
)


def test_list_skills(client, db_session):
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

    create_skill(
        db_session,
        resume_id=resume.id,
        name="Python",
    )

    create_skill(
        db_session,
        resume_id=resume.id,
        name="FastAPI",
    )

    login = client.post(
        "/auth/login",
        data={
            "username": user.email,
            "password": DEFAULT_PASSWORD,
        },
    )

    assert login.status_code == 200

    token = login.json()["access_token"]

    response = client.get(
        f"/api/skills/resume/{resume.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["skills"]) == 2
    assert data["skills"][0]["name"] == "Python"
    assert data["skills"][1]["name"] == "FastAPI"


def test_list_returns_only_resume_skills(
    client,
    db_session,
):
    user = create_user(
        db_session,
        verified=True,
    )

    resume_one = create_resume(
        db_session,
        user_id=user.id,
    )

    resume_two = create_resume(
        db_session,
        user_id=user.id,
        title="Second Resume",
    )

    create_skill(
        db_session,
        resume_id=resume_one.id,
        name="Python",
    )

    create_skill(
        db_session,
        resume_id=resume_two.id,
        name="Docker",
    )

    login = client.post(
        "/auth/login",
        data={
            "username": user.email,
            "password": DEFAULT_PASSWORD,
        },
    )

    assert login.status_code == 200

    token = login.json()["access_token"]

    response = client.get(
        f"/api/skills/resume/{resume_one.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["skills"]) == 1
    assert data["skills"][0]["name"] == "Python"


def test_cannot_list_another_users_resume_skills(
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

    create_skill(
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

    assert login.status_code == 200

    token = login.json()["access_token"]

    response = client.get(
        f"/api/skills/resume/{resume.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 403
