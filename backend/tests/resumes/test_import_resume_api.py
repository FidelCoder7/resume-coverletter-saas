from app.common.constants import ResumeVersionSource


def test_import_resume_creates_complete_resume_and_import_version(
    authenticated_client,
    db_session,
):
    client, user = authenticated_client

    response = client.post(
        "/api/resumes/import",
        json={
            "title": "Imported Backend Engineer Resume",
            "summary": "Backend engineer with Python experience.",
            "experiences": [
                {
                    "company": "Acme",
                    "job_title": "Backend Engineer",
                    "location": "Nairobi",
                    "employment_type": "full_time",
                    "start_date": "2023-01-01",
                    "end_date": None,
                    "is_current": True,
                    "description": "Built backend APIs.",
                    "display_order": 0,
                },
            ],
            "educations": [
                {
                    "institution": "University",
                    "degree": "BSc Computer Science",
                    "field_of_study": "Computer Science",
                    "location": "Nairobi",
                    "grade": "First Class",
                    "start_date": "2019-01-01",
                    "end_date": "2023-01-01",
                    "is_current": False,
                    "description": None,
                    "display_order": 0,
                },
            ],
            "skills": [
                {
                    "name": "Python",
                    "proficiency": "advanced",
                    "display_order": 0,
                },
            ],
            "projects": [
                {
                    "name": "Resume SaaS",
                    "description": "AI-powered resume platform.",
                    "technologies": "Python, FastAPI, PostgreSQL",
                    "project_url": "https://example.com/project",
                    "repository_url": ("https://github.com/example/resume-saas"),
                    "start_date": "2024-01-01",
                    "end_date": None,
                    "is_ongoing": True,
                    "display_order": 0,
                },
            ],
            "certifications": [
                {
                    "name": "AWS Certified Cloud Practitioner",
                    "issuing_organization": "Amazon Web Services",
                    "credential_id": "ABC123",
                    "credential_url": ("https://example.com/certificate"),
                    "issue_date": "2024-01-01",
                    "expiration_date": None,
                    "does_not_expire": True,
                    "display_order": 0,
                },
            ],
        },
    )

    assert response.status_code == 201

    body = response.json()

    resume_id = body["id"]

    assert body["user_id"] == str(user.id)
    assert body["title"] == "Imported Backend Engineer Resume"
    assert body["summary"] == ("Backend engineer with Python experience.")

    versions_response = client.get(
        f"/api/resumes/{resume_id}/versions",
    )

    assert versions_response.status_code == 200

    versions = versions_response.json()

    assert len(versions) == 1

    version = versions[0]

    assert version["version_number"] == 1
    assert version["source"] == ResumeVersionSource.IMPORT.value
    assert version["change_summary"] == ("Resume imported by user.")

    snapshot = version["snapshot"]

    assert snapshot["title"] == ("Imported Backend Engineer Resume")

    assert snapshot["summary"] == ("Backend engineer with Python experience.")

    assert len(snapshot["experiences"]) == 1
    assert snapshot["experiences"][0]["company"] == "Acme"

    assert len(snapshot["educations"]) == 1
    assert snapshot["educations"][0]["institution"] == "University"

    assert len(snapshot["skills"]) == 1
    assert snapshot["skills"][0]["name"] == "Python"

    assert len(snapshot["projects"]) == 1
    assert snapshot["projects"][0]["name"] == "Resume SaaS"

    assert len(snapshot["certifications"]) == 1
    assert snapshot["certifications"][0]["name"] == "AWS Certified Cloud Practitioner"


def test_import_resume_creates_empty_resume_when_no_children_are_supplied(
    authenticated_client,
):
    client, _ = authenticated_client

    response = client.post(
        "/api/resumes/import",
        json={
            "title": "Minimal Imported Resume",
        },
    )

    assert response.status_code == 201

    resume_id = response.json()["id"]

    versions_response = client.get(
        f"/api/resumes/{resume_id}/versions",
    )

    assert versions_response.status_code == 200

    versions = versions_response.json()

    assert len(versions) == 1
    assert versions[0]["version_number"] == 1
    assert versions[0]["source"] == (ResumeVersionSource.IMPORT.value)

    snapshot = versions[0]["snapshot"]

    assert snapshot["title"] == "Minimal Imported Resume"
    assert snapshot["experiences"] == []
    assert snapshot["educations"] == []
    assert snapshot["skills"] == []
    assert snapshot["projects"] == []
    assert snapshot["certifications"] == []


def test_import_resume_requires_authentication():
    from fastapi.testclient import TestClient

    from app.main import app

    client = TestClient(app)

    response = client.post(
        "/api/resumes/import",
        json={
            "title": "Unauthenticated Import",
        },
    )

    assert response.status_code in (401, 403)


def test_import_resume_rejects_invalid_payload(
    authenticated_client,
):
    client, _ = authenticated_client

    response = client.post(
        "/api/resumes/import",
        json={
            "title": "",
        },
    )

    assert response.status_code == 422
