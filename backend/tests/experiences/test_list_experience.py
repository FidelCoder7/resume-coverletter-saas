from tests.factories.experience_factory import create_experience
from tests.factories.resume_factory import create_resume
from tests.factories.user_factory import (
    DEFAULT_PASSWORD,
    create_user,
)


def test_list_experiences(client, db_session):
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

    create_experience(
        db_session,
        resume_id=resume.id,
        company="Google",
    )

    create_experience(
        db_session,
        resume_id=resume.id,
        company="Microsoft",
    )

    login = client.post(
        "/auth/login",
        data={
            "username": user.email,
            "password": DEFAULT_PASSWORD,
        },
    )

    token = login.json()["access_token"]

    response = client.get(
        f"/api/experiences/resume/{resume.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["experiences"]) == 2


def test_list_returns_only_resume_experiences(
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

    create_experience(
        db_session,
        resume_id=resume_one.id,
        company="OpenAI",
    )

    create_experience(
        db_session,
        resume_id=resume_two.id,
        company="Google",
    )

    login = client.post(
        "/auth/login",
        data={
            "username": user.email,
            "password": DEFAULT_PASSWORD,
        },
    )

    token = login.json()["access_token"]

    response = client.get(
        f"/api/experiences/resume/{resume_one.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["experiences"]) == 1
    assert data["experiences"][0]["company"] == "OpenAI"


def test_cannot_list_another_users_resume_experiences(
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

    create_experience(
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

    response = client.get(
        f"/api/experiences/resume/{resume.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 403
