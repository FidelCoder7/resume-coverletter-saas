from tests.factories.resume_factory import create_resume
from tests.factories.user_factory import DEFAULT_PASSWORD, create_user


def test_create_education(client, db_session):
    user = create_user(
        db_session,
        email="john@example.com",
        password=DEFAULT_PASSWORD,
        verified=True,
    )

    resume = create_resume(
        db_session,
        user_id=user.id,
        title="Backend Resume",
        summary="Python Developer",
    )

    login = client.post(
        "/auth/login",
        data={
            "username": user.email,
            "password": DEFAULT_PASSWORD,
        },
    )

    token = login.json()["access_token"]

    response = client.post(
        f"/api/educations/resume/{resume.id}",
        json={
            "institution": "University of Nairobi",
            "degree": "Bachelor of Science",
            "field_of_study": "Computer Science",
            "location": "Nairobi",
            "grade": "First Class",
            "start_date": "2022-09-01",
            "end_date": None,
            "is_current": True,
            "description": "Relevant coursework and final year project.",
            "display_order": 0,
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["resume_id"] == str(resume.id)
    assert data["institution"] == "University of Nairobi"
    assert data["degree"] == "Bachelor of Science"
    assert data["field_of_study"] == "Computer Science"


## Authentication Test


def test_create_education_requires_authentication(client, db_session):
    user = create_user(
        db_session,
        verified=True,
    )

    resume = create_resume(
        db_session,
        user_id=user.id,
    )

    response = client.post(
        f"/api/educations/resume/{resume.id}",
        json={
            "institution": "University of Nairobi",
            "degree": "Bachelor of Science",
            "field_of_study": "Computer Science",
            "start_date": "2022-09-01",
            "is_current": True,
            "display_order": 0,
        },
    )

    assert response.status_code == 401
