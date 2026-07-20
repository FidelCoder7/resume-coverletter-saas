from app.ai.prompts import (
    ATSOptimizationPromptBuilder,
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

    _ats_optimization_builders: dict[
        str,
        type[ATSOptimizationPromptBuilder],
    ] = {
        "ats_optimization_v1": ATSOptimizationPromptBuilder,
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

    @classmethod
    def get_ats_optimization_prompt_builder(
        cls,
        version: str,
    ) -> type[ATSOptimizationPromptBuilder]:
        """
        Return the prompt builder for the requested ATS optimization
        prompt version.
        """

        try:
            return cls._ats_optimization_builders[version]
        except KeyError as exc:
            raise ValueError(
                f"Unsupported ATS optimization prompt version: {version}",
            ) from exc
