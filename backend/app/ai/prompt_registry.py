from app.ai.prompts import (
    CoverLetterPromptBuilder,
    ResumePromptBuilder,
)


class PromptRegistry:
    """
    Registry of available prompt builders.

    This centralizes prompt version resolution and provides a single
    location for registering future prompt implementations.
    """

    _resume_builders: dict[str, type[ResumePromptBuilder]] = {
        "resume_v1": ResumePromptBuilder,
    }

    _cover_letter_builders: dict[str, type[CoverLetterPromptBuilder]] = {
        "cover_letter_v1": CoverLetterPromptBuilder,
    }

    @classmethod
    def get_resume_prompt_builder(
        cls,
        version: str,
    ) -> type[ResumePromptBuilder]:
        """
        Return the prompt builder for the requested resume prompt version.
        """

        try:
            return cls._resume_builders[version]
        except KeyError as exc:
            raise ValueError(
                f"Unsupported resume prompt version: {version}",
            ) from exc

    @classmethod
    def get_cover_letter_prompt_builder(
        cls,
        version: str,
    ) -> type[CoverLetterPromptBuilder]:
        """
        Return the prompt builder for the requested cover letter prompt version.
        """

        try:
            return cls._cover_letter_builders[version]
        except KeyError as exc:
            raise ValueError(
                f"Unsupported cover letter prompt version: {version}",
            ) from exc
