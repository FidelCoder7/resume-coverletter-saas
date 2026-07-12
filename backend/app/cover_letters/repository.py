from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.cover_letters.exceptions import DuplicateCoverLetter
from app.cover_letters.models import CoverLetter


class CoverLetterRepository:
    """
    Repository for cover letter persistence.
    """

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def create(
        self,
        cover_letter: CoverLetter,
    ) -> CoverLetter:
        self.db.add(cover_letter)

        try:
            self.db.commit()
        except IntegrityError as exc:
            self.db.rollback()

            if "uq_cover_letter_resume_title" in str(exc.orig):
                raise DuplicateCoverLetter(
                    "A cover letter with this title already exists on this resume."
                ) from None

            raise

        self.db.refresh(cover_letter)

        return cover_letter

    def get_by_id(
        self,
        cover_letter_id: UUID,
    ) -> CoverLetter | None:
        statement = select(CoverLetter).where(
            CoverLetter.id == cover_letter_id,
        )

        return self.db.scalar(statement)

    def list_by_resume(
        self,
        resume_id: UUID,
    ) -> list[CoverLetter]:
        statement = (
            select(CoverLetter)
            .where(
                CoverLetter.resume_id == resume_id,
            )
            .order_by(
                CoverLetter.updated_at.desc(),
                CoverLetter.created_at.desc(),
            )
        )

        return list(self.db.scalars(statement))

    def update(
        self,
        cover_letter: CoverLetter,
    ) -> CoverLetter:
        try:
            self.db.commit()
        except IntegrityError as exc:
            self.db.rollback()

            if "uq_cover_letter_resume_title" in str(exc.orig):
                raise DuplicateCoverLetter(
                    "A cover letter with this title already exists on this resume."
                ) from None

            raise

        self.db.refresh(cover_letter)

        return cover_letter

    def delete(
        self,
        cover_letter: CoverLetter,
    ) -> None:
        self.db.delete(cover_letter)
        self.db.commit()
