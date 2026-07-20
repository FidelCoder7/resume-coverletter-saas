import re
from collections import Counter

_WORD_PATTERN = re.compile(r"\b[a-zA-Z][a-zA-Z0-9+#.\-]{1,}\b")


class ATSScoringService:
    """
    Calculates ATS keyword matching scores.
    """

    @staticmethod
    def tokenize(
        text: str,
    ) -> list[str]:
        return [token.lower() for token in _WORD_PATTERN.findall(text)]

    @classmethod
    def extract_keywords(
        cls,
        text: str,
    ) -> list[str]:
        tokens = cls.tokenize(text)

        counts = Counter(tokens)

        return sorted(
            counts.keys(),
        )

    @classmethod
    def score(
        cls,
        *,
        resume: str,
        job_description: str,
    ) -> tuple[
        int,
        list[str],
        list[str],
    ]:
        resume_keywords = set(
            cls.extract_keywords(
                resume,
            )
        )

        job_keywords = set(
            cls.extract_keywords(
                job_description,
            )
        )

        if not job_keywords:
            return (
                100,
                [],
                [],
            )

        matched = sorted(
            resume_keywords & job_keywords,
        )

        missing = sorted(
            job_keywords - resume_keywords,
        )

        score = int(len(matched) / len(job_keywords) * 100)

        return (
            score,
            matched,
            missing,
        )
