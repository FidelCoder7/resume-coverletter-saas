from tests.factories.cover_letter_factory import create_cover_letter
from tests.factories.resume_factory import create_resume
from tests.factories.user_factory import (
    DEFAULT_PASSWORD,
    create_user,
)


def test_list_cover_letters(
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

    create_cover_letter(
        db_session,
        resume_id=resume.id,
        title="Backend Engineer",
        company_name="OpenAI",
    )

    create_cover_letter(
        db_session,
        resume_id=resume.id,
        title="Software Engineer",
        company_name="Microsoft",
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
        f"/api/cover-letters/resume/{resume.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["cover_letters"]) == 2
    assert data["cover_letters"][0]["title"] == "Backend Engineer"
    assert data["cover_letters"][1]["title"] == "Software Engineer"


def test_list_returns_only_resume_cover_letters(
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

    create_cover_letter(
        db_session,
        resume_id=resume_one.id,
        title="Backend Engineer",
    )

    create_cover_letter(
        db_session,
        resume_id=resume_two.id,
        title="Frontend Engineer",
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
        f"/api/cover-letters/resume/{resume_one.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["cover_letters"]) == 1
    assert data["cover_letters"][0]["title"] == "Backend Engineer"


def test_list_empty_cover_letters(
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
        f"/api/cover-letters/resume/{resume.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    assert response.json() == {"cover_letters": []}


def test_cannot_list_another_users_cover_letters(
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

    create_cover_letter(
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
        f"/api/cover-letters/resume/{resume.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 403

    assert response.json() == {
        "detail": "You do not have permission to modify this resume."
    }
