from app.ai.prompt_registry import PromptRegistry
from app.ai.schemas import (
    ATSOptimizationRequest,
    CoverLetterGenerationRequest,
    ResumeGenerationRequest,
)


class PromptService:
    """
    Builds provider-ready chat messages for AI requests.

    Prompt builders are resolved through the PromptRegistry, allowing
    prompt implementations to evolve independently of providers.
    """

    @staticmethod
    def build_cover_letter_messages(
        request: CoverLetterGenerationRequest,
        *,
        version: str,
    ) -> list[dict[str, str]]:
        """
        Build chat messages for cover letter generation.
        """

        builder = PromptRegistry.get_cover_letter_prompt_builder(
            version,
        )

        return [
            {
                "role": "system",
                "content": builder.build_system_prompt(),
            },
            {
                "role": "user",
                "content": builder.build_user_prompt(
                    request,
                ),
            },
        ]

    @staticmethod
    def build_resume_messages(
        request: ResumeGenerationRequest,
        *,
        version: str,
    ) -> list[dict[str, str]]:
        """
        Build chat messages for resume generation.
        """

        builder = PromptRegistry.get_resume_prompt_builder(
            version,
        )

        return [
            {
                "role": "system",
                "content": builder.build_system_prompt(),
            },
            {
                "role": "user",
                "content": builder.build_user_prompt(
                    request,
                ),
            },
        ]

    @staticmethod
    def build_ats_optimization_messages(
        request: ATSOptimizationRequest,
        *,
        version: str,
    ) -> list[dict[str, str]]:
        """
        Build chat messages for ATS resume optimization.
        """

        builder = PromptRegistry.get_ats_optimization_prompt_builder(
            version,
        )

        return [
            {
                "role": "system",
                "content": builder.build_system_prompt(),
            },
            {
                "role": "user",
                "content": builder.build_user_prompt(
                    request,
                ),
            },
        ]
