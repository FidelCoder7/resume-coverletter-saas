from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.certifications.exceptions import DuplicateCertification
from app.certifications.models import Certification


class CertificationRepository:
    """
    Repository for certification persistence.
    """

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def create(
        self,
        certification: Certification,
    ) -> Certification:
        self.db.add(certification)

        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise DuplicateCertification(
                "A certification with this name already exists on this resume."
            ) from None

        self.db.refresh(certification)

        return certification

    def get_by_id(
        self,
        certification_id: UUID,
    ) -> Certification | None:
        statement = select(Certification).where(
            Certification.id == certification_id,
        )

        return self.db.scalar(statement)

    def list_by_resume(
        self,
        resume_id: UUID,
    ) -> list[Certification]:
        statement = (
            select(Certification)
            .where(
                Certification.resume_id == resume_id,
            )
            .order_by(
                Certification.display_order.asc(),
                Certification.created_at.asc(),
            )
        )

        return list(self.db.scalars(statement))

    def update(
        self,
        certification: Certification,
    ) -> Certification:
        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise DuplicateCertification(
                "A certification with this name already exists on this resume."
            ) from None

        self.db.refresh(certification)

        return certification

    def delete(
        self,
        certification: Certification,
    ) -> None:
        self.db.delete(certification)
        self.db.commit()
