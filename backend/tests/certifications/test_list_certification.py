from tests.factories.certification_factory import create_certification
from tests.factories.resume_factory import create_resume
from tests.factories.user_factory import (
    DEFAULT_PASSWORD,
    create_user,
)


def test_list_certifications(client, db_session):
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

    create_certification(
        db_session,
        resume_id=resume.id,
        name="AWS Certified Developer - Associate",
        display_order=0,
    )

    create_certification(
        db_session,
        resume_id=resume.id,
        name="Microsoft Azure Fundamentals",
        display_order=1,
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
        f"/api/certifications/resume/{resume.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["certifications"]) == 2
    assert data["certifications"][0]["name"] == "AWS Certified Developer - Associate"
    assert data["certifications"][1]["name"] == "Microsoft Azure Fundamentals"


def test_list_returns_only_resume_certifications(
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

    create_certification(
        db_session,
        resume_id=resume_one.id,
        name="AWS Certified Developer - Associate",
    )

    create_certification(
        db_session,
        resume_id=resume_two.id,
        name="Microsoft Azure Fundamentals",
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
        f"/api/certifications/resume/{resume_one.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["certifications"]) == 1
    assert data["certifications"][0]["name"] == "AWS Certified Developer - Associate"


def test_cannot_list_another_users_resume_certifications(
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

    create_certification(
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
        f"/api/certifications/resume/{resume.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 403


def test_list_certifications_orders_by_display_order(
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

    create_certification(
        db_session,
        resume_id=resume.id,
        name="Third",
        display_order=5,
    )

    create_certification(
        db_session,
        resume_id=resume.id,
        name="First",
        display_order=0,
    )

    create_certification(
        db_session,
        resume_id=resume.id,
        name="Second",
        display_order=2,
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
        f"/api/certifications/resume/{resume.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    certifications = response.json()["certifications"]

    assert certifications[0]["name"] == "First"
    assert certifications[1]["name"] == "Second"
    assert certifications[2]["name"] == "Third"

    assert certifications[0]["display_order"] == 0
    assert certifications[1]["display_order"] == 2
    assert certifications[2]["display_order"] == 5
