from datetime import date
from uuid import UUID

from app.certifications.exceptions import (
    CertificationAccessDenied,
    CertificationNotFound,
    InvalidCertificationDate,
)
from app.certifications.models import Certification
from app.certifications.repository import CertificationRepository
from app.resumes.repository import ResumeRepository


class CertificationService:
    """
    Business logic for resume certification management.
    """

    def __init__(
        self,
        repository: CertificationRepository,
        resume_repository: ResumeRepository,
    ):
        self.repository = repository
        self.resume_repository = resume_repository

    def _verify_resume_owner(
        self,
        *,
        resume_id: UUID,
        user_id: UUID,
    ):
        """
        Ensure the resume belongs to the authenticated user.
        """

        resume = self.resume_repository.get_by_id(
            resume_id,
        )

        if resume is None:
            raise CertificationNotFound(
                "Resume not found.",
            )

        if resume.user_id != user_id:
            raise CertificationAccessDenied(
                "You do not have permission to modify this resume.",
            )

        return resume

    def _validate_dates(
        self,
        *,
        issue_date: date,
        expiration_date: date | None,
        does_not_expire: bool,
    ) -> None:
        """
        Validate certification date business rules.
        """

        if does_not_expire and expiration_date is not None:
            raise InvalidCertificationDate(
                "A certification that does not expire cannot have an expiration date.",
            )

        if expiration_date is not None and expiration_date < issue_date:
            raise InvalidCertificationDate(
                "Expiration date cannot be earlier than issue date.",
            )

        if issue_date > date.today():
            raise InvalidCertificationDate(
                "Issue date cannot be in the future.",
            )

    def create_certification(
        self,
        *,
        user_id: UUID,
        resume_id: UUID,
        name: str,
        issuing_organization: str,
        credential_id: str | None,
        credential_url: str | None,
        issue_date: date,
        expiration_date: date | None,
        does_not_expire: bool,
        display_order: int,
    ) -> Certification:
        self._verify_resume_owner(
            resume_id=resume_id,
            user_id=user_id,
        )

        self._validate_dates(
            issue_date=issue_date,
            expiration_date=expiration_date,
            does_not_expire=does_not_expire,
        )

        certification = Certification(
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

        return self.repository.create(
            certification,
        )

    def list_certifications(
        self,
        *,
        user_id: UUID,
        resume_id: UUID,
    ) -> list[Certification]:
        self._verify_resume_owner(
            resume_id=resume_id,
            user_id=user_id,
        )

        return self.repository.list_by_resume(
            resume_id,
        )

    def get_certification(
        self,
        *,
        user_id: UUID,
        certification_id: UUID,
    ) -> Certification:
        certification = self.repository.get_by_id(
            certification_id,
        )

        if certification is None:
            raise CertificationNotFound(
                "Certification not found.",
            )

        self._verify_resume_owner(
            resume_id=certification.resume_id,
            user_id=user_id,
        )

        return certification

    def update_certification(
        self,
        *,
        user_id: UUID,
        certification_id: UUID,
        name: str,
        issuing_organization: str,
        credential_id: str | None,
        credential_url: str | None,
        issue_date: date,
        expiration_date: date | None,
        does_not_expire: bool,
        display_order: int,
    ) -> Certification:
        certification = self.get_certification(
            user_id=user_id,
            certification_id=certification_id,
        )

        self._validate_dates(
            issue_date=issue_date,
            expiration_date=expiration_date,
            does_not_expire=does_not_expire,
        )

        certification.name = name
        certification.issuing_organization = issuing_organization
        certification.credential_id = credential_id
        certification.credential_url = credential_url
        certification.issue_date = issue_date
        certification.expiration_date = expiration_date
        certification.does_not_expire = does_not_expire
        certification.display_order = display_order

        return self.repository.update(
            certification,
        )

    def delete_certification(
        self,
        *,
        user_id: UUID,
        certification_id: UUID,
    ) -> None:
        certification = self.get_certification(
            user_id=user_id,
            certification_id=certification_id,
        )

        self.repository.delete(
            certification,
        )
