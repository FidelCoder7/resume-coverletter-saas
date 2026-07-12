from uuid import uuid4

from tests.factories.certification_factory import create_certification
from tests.factories.resume_factory import create_resume
from tests.factories.user_factory import (
    DEFAULT_PASSWORD,
    create_user,
)


def test_delete_certification(client, db_session):
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

    certification = create_certification(
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

    assert login.status_code == 200

    token = login.json()["access_token"]

    response = client.delete(
        f"/api/certifications/{certification.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 204

    response = client.get(
        f"/api/certifications/{certification.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 404


def test_cannot_delete_another_users_certification(
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

    certification = create_certification(
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

    response = client.delete(
        f"/api/certifications/{certification.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 403


def test_delete_unknown_certification_returns_404(
    client,
    db_session,
):
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

    assert login.status_code == 200

    token = login.json()["access_token"]

    response = client.delete(
        f"/api/certifications/{uuid4()}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 404
