from app.resumes.models import Resume
from tests.factories.education_factory import create_education
from tests.factories.user_factory import (
    DEFAULT_PASSWORD,
    create_user,
)


def test_list_educations(
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

    create_education(
        db_session,
        resume_id=resume.id,
        institution="University A",
        degree="BSc Computer Science",
        display_order=0,
    )

    create_education(
        db_session,
        resume_id=resume.id,
        institution="University B",
        degree="MSc Software Engineering",
        display_order=1,
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
        f"/api/educations/resume/{resume.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["institution"] == "University A"
    assert data[1]["institution"] == "University B"


def test_list_educations_empty(
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

    token = login.json()["access_token"]

    response = client.get(
        f"/api/educations/resume/{resume.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200
    assert response.json() == []


def test_list_educations_requires_authentication(
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

    response = client.get(
        f"/api/educations/resume/{resume.id}",
    )

    assert response.status_code == 401
