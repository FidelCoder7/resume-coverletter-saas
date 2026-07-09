from tests.factories.education_factory import create_education
from tests.factories.resume_factory import create_resume
from tests.factories.user_factory import (
    DEFAULT_PASSWORD,
    create_user,
)


def test_update_education(
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
    )

    login = client.post(
        "/auth/login",
        data={
            "username": user.email,
            "password": DEFAULT_PASSWORD,
        },
    )

    token = login.json()["access_token"]

    response = client.put(
        f"/api/educations/{education.id}",
        json={
            "institution": "Stanford University",
            "degree": "Master of Science",
            "field_of_study": "Artificial Intelligence",
            "location": "California",
            "grade": "4.0 GPA",
            "start_date": "2021-09-01",
            "end_date": "2023-06-30",
            "is_current": False,
            "description": "Focused on machine learning.",
            "display_order": 1,
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["institution"] == "Stanford University"
    assert data["degree"] == "Master of Science"
    assert data["field_of_study"] == "Artificial Intelligence"
    assert data["location"] == "California"
    assert data["grade"] == "4.0 GPA"
    assert data["display_order"] == 1


def test_update_education_requires_authentication(
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

    response = client.put(
        f"/api/educations/{education.id}",
        json={
            "institution": "Updated University",
            "degree": "Updated Degree",
            "field_of_study": "Updated Field",
            "location": "Updated Location",
            "grade": "Updated Grade",
            "start_date": "2021-01-01",
            "end_date": "2023-01-01",
            "is_current": False,
            "description": "Updated description.",
            "display_order": 0,
        },
    )

    assert response.status_code == 401
