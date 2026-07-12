from uuid import uuid4

from tests.factories.certification_factory import create_certification
from tests.factories.resume_factory import create_resume
from tests.factories.user_factory import (
    DEFAULT_PASSWORD,
    create_user,
)


def test_get_certification(client, db_session):
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

    response = client.get(
        f"/api/certifications/{certification.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(certification.id)
    assert data["resume_id"] == str(resume.id)
    assert data["name"] == certification.name
    assert data["issuing_organization"] == certification.issuing_organization
    assert data["credential_id"] == certification.credential_id
    assert data["credential_url"] == str(certification.credential_url)
    assert data["issue_date"] == str(certification.issue_date)
    assert data["expiration_date"] is None
    assert data["does_not_expire"] == certification.does_not_expire
    assert data["display_order"] == certification.display_order


def test_cannot_get_another_users_certification(
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

    response = client.get(
        f"/api/certifications/{certification.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 403


def test_get_unknown_certification_returns_404(
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

    response = client.get(
        f"/api/certifications/{uuid4()}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 404
