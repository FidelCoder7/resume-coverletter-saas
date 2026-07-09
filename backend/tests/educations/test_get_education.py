from tests.factories.education_factory import create_education
from tests.factories.resume_factory import create_resume
from tests.factories.user_factory import (
    DEFAULT_PASSWORD,
    create_user,
)


def test_get_education(
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
        institution="MIT",
        degree="BSc Computer Science",
        field_of_study="Computer Science",
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
        f"/api/educations/{education.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(education.id)
    assert data["institution"] == "MIT"
    assert data["degree"] == "BSc Computer Science"
    assert data["field_of_study"] == "Computer Science"


def test_get_education_requires_authentication(
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

    response = client.get(
        f"/api/educations/{education.id}",
    )

    assert response.status_code == 401
