from tests.factories.resume_factory import create_resume
from tests.factories.resume_version_factory import create_resume_version


def test_list_resume_versions_returns_newest_first(
    authenticated_client,
    db_session,
):
    client, user = authenticated_client

    resume = create_resume(
        db_session,
        user_id=user.id,
    )

    create_resume_version(
        db_session,
        resume_id=resume.id,
        version_number=1,
        snapshot={"title": "Version 1"},
    )

    create_resume_version(
        db_session,
        resume_id=resume.id,
        version_number=2,
        snapshot={"title": "Version 2"},
    )

    create_resume_version(
        db_session,
        resume_id=resume.id,
        version_number=3,
        snapshot={"title": "Version 3"},
    )

    response = client.get(
        f"/api/resumes/{resume.id}/versions",
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 3

    assert [item["version_number"] for item in data] == [
        3,
        2,
        1,
    ]

    assert data[0]["snapshot"] == {
        "title": "Version 3",
    }
