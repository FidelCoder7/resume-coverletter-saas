from app.resumes.models import Resume
from tests.factories.user_factory import DEFAULT_PASSWORD, create_user


def test_create_experience(client, db_session):
    user = create_user(
        db_session,
        email="john@example.com",
        password=DEFAULT_PASSWORD,
        verified=True,
    )

    resume = Resume(
        user_id=user.id,
        title="Backend Resume",
        summary="Python Developer",
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

    response = client.post(
        f"/api/experiences/resume/{resume.id}",
        json={
            "company": "OpenAI",
            "job_title": "Software Engineer",
            "location": "Remote",
            "employment_type": "full_time",
            "start_date": "2024-01-01",
            "end_date": None,
            "is_current": True,
            "description": "Built AI APIs.",
            "display_order": 0,
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["company"] == "OpenAI"
    assert data["job_title"] == "Software Engineer"
    assert data["resume_id"] == str(resume.id)


def test_create_experience_requires_authentication(client, db_session):
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
        f"/api/experiences/resume/{resume.id}",
        json={
            "company": "OpenAI",
            "job_title": "Engineer",
            "employment_type": "full_time",
            "start_date": "2024-01-01",
            "is_current": True,
            "display_order": 0,
        },
    )

    assert response.status_code == 401
