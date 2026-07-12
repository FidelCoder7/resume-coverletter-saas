from uuid import uuid4

from tests.factories.certification_factory import create_certification
from tests.factories.resume_factory import create_resume
from tests.factories.user_factory import (
    DEFAULT_PASSWORD,
    create_user,
)


def test_update_certification(client, db_session):
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

    response = client.put(
        f"/api/certifications/{certification.id}",
        json={
            "name": "AWS Certified Solutions Architect - Associate",
            "issuing_organization": "Amazon Web Services",
            "credential_id": "XYZ987654321",
            "credential_url": "https://www.credly.com/",
            "issue_date": "2025-01-01",
            "expiration_date": "2028-01-01",
            "does_not_expire": False,
            "display_order": 1,
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "AWS Certified Solutions Architect - Associate"
    assert data["issuing_organization"] == "Amazon Web Services"
    assert data["credential_id"] == "XYZ987654321"
    assert data["credential_url"] == "https://www.credly.com/"
    assert data["issue_date"] == "2025-01-01"
    assert data["expiration_date"] == "2028-01-01"
    assert data["does_not_expire"] is False
    assert data["display_order"] == 1


def test_cannot_update_another_users_certification(
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

    response = client.put(
        f"/api/certifications/{certification.id}",
        json={
            "name": "Unauthorized Update",
            "issuing_organization": "AWS",
            "credential_id": "123456",
            "credential_url": "https://www.credly.com/",
            "issue_date": "2025-01-01",
            "expiration_date": None,
            "does_not_expire": True,
            "display_order": 0,
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 403


def test_update_unknown_certification_returns_404(
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

    response = client.put(
        f"/api/certifications/{uuid4()}",
        json={
            "name": "AWS Certification",
            "issuing_organization": "AWS",
            "credential_id": "123456",
            "credential_url": "https://www.credly.com/",
            "issue_date": "2025-01-01",
            "expiration_date": None,
            "does_not_expire": True,
            "display_order": 0,
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 404


def test_update_certification_rejects_invalid_dates(
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

    response = client.put(
        f"/api/certifications/{certification.id}",
        json={
            "name": "AWS Certification",
            "issuing_organization": "AWS",
            "credential_id": "123456",
            "credential_url": "https://www.credly.com/",
            "issue_date": "2025-06-01",
            "expiration_date": "2025-01-01",
            "does_not_expire": False,
            "display_order": 0,
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 400


def test_update_non_expiring_certification_cannot_have_expiration_date(
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

    response = client.put(
        f"/api/certifications/{certification.id}",
        json={
            "name": "AWS Certification",
            "issuing_organization": "AWS",
            "credential_id": "123456",
            "credential_url": "https://www.credly.com/",
            "issue_date": "2025-01-01",
            "expiration_date": "2028-01-01",
            "does_not_expire": True,
            "display_order": 0,
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 400
