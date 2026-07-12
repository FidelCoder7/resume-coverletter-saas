from app.resumes.models import Resume
from tests.factories.user_factory import (
    DEFAULT_PASSWORD,
    create_user,
)


def test_create_certification(client, db_session):
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
        f"/api/certifications/resume/{resume.id}",
        json={
            "name": "AWS Certified Developer - Associate",
            "issuing_organization": "Amazon Web Services",
            "credential_id": "ABC123456789",
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

    assert response.status_code == 201

    data = response.json()

    assert data["resume_id"] == str(resume.id)
    assert data["name"] == "AWS Certified Developer - Associate"
    assert data["issuing_organization"] == "Amazon Web Services"
    assert data["credential_id"] == "ABC123456789"
    assert data["credential_url"] == "https://www.credly.com/"
    assert data["issue_date"] == "2025-01-01"
    assert data["expiration_date"] is None
    assert data["does_not_expire"] is True
    assert data["display_order"] == 0


def test_create_certification_requires_authentication(
    client,
    db_session,
):
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
        f"/api/certifications/resume/{resume.id}",
        json={
            "name": "AWS Certified Developer - Associate",
            "issuing_organization": "Amazon Web Services",
            "credential_id": "ABC123456789",
            "credential_url": "https://www.credly.com/",
            "issue_date": "2025-01-01",
            "expiration_date": None,
            "does_not_expire": True,
            "display_order": 0,
        },
    )

    assert response.status_code == 401


def test_create_certification_rejects_invalid_dates(
    client,
    db_session,
):
    user = create_user(
        db_session,
        email="john@example.com",
        password=DEFAULT_PASSWORD,
        verified=True,
    )

    resume = Resume(
        user_id=user.id,
        title="Backend Resume",
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
        f"/api/certifications/resume/{resume.id}",
        json={
            "name": "AWS Certified Developer - Associate",
            "issuing_organization": "Amazon Web Services",
            "credential_id": "ABC123456789",
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


def test_create_non_expiring_certification_cannot_have_expiration_date(
    client,
    db_session,
):
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
        f"/api/certifications/resume/{resume.id}",
        json={
            "name": "AWS Certified Developer - Associate",
            "issuing_organization": "Amazon Web Services",
            "credential_id": "ABC123456789",
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


def test_cannot_create_duplicate_certification_name_for_same_resume(
    client,
    db_session,
):
    user = create_user(
        db_session,
        email="john@example.com",
        password=DEFAULT_PASSWORD,
        verified=True,
    )

    resume = Resume(
        user_id=user.id,
        title="Backend Resume",
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

    payload = {
        "name": "AWS Certified Developer - Associate",
        "issuing_organization": "Amazon Web Services",
        "credential_id": "ABC123456",
        "credential_url": "https://www.credly.com/",
        "issue_date": "2025-01-01",
        "expiration_date": None,
        "does_not_expire": True,
        "display_order": 0,
    }

    response = client.post(
        f"/api/certifications/resume/{resume.id}",
        json=payload,
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 201

    response = client.post(
        f"/api/certifications/resume/{resume.id}",
        json=payload,
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 409

    assert response.json() == {
        "detail": ("A certification with this name already exists on this resume.")
    }


def test_create_certification_rejects_invalid_credential_url(
    client,
    db_session,
):
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
        f"/api/certifications/resume/{resume.id}",
        json={
            "name": "AWS Certification",
            "issuing_organization": "AWS",
            "credential_id": "ABC123",
            "credential_url": "not-a-valid-url",
            "issue_date": "2025-01-01",
            "expiration_date": None,
            "does_not_expire": True,
            "display_order": 0,
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 422
