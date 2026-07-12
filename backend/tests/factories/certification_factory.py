from datetime import date

from app.certifications.models import Certification


def make_certification(
    *,
    resume_id,
    name: str = "AWS Certified Developer - Associate",
    issuing_organization: str = "Amazon Web Services",
    credential_id: str | None = "ABC123456789",
    credential_url: str | None = "https://www.credly.com/",
    issue_date: date = date(2025, 1, 1),
    expiration_date: date | None = None,
    does_not_expire: bool = True,
    display_order: int = 0,
) -> Certification:
    return Certification(
        resume_id=resume_id,
        name=name,
        issuing_organization=issuing_organization,
        credential_id=credential_id,
        credential_url=credential_url,
        issue_date=issue_date,
        expiration_date=expiration_date,
        does_not_expire=does_not_expire,
        display_order=display_order,
    )


def create_certification(
    db,
    *,
    resume_id,
    **kwargs,
) -> Certification:
    certification = make_certification(
        resume_id=resume_id,
        **kwargs,
    )

    db.add(certification)
    db.commit()
    db.refresh(certification)

    return certification
