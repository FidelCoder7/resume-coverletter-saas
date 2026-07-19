from openai import OpenAI

from app.ai.base_chat_provider import BaseChatProvider
from app.ai.config import AISettings
from app.ai.contracts import AIExecutionResult
from app.ai.exceptions import AIConfigurationError
from app.ai.prompt_service import PromptService
from app.ai.provider_capabilities import ProviderCapabilities
from app.ai.providers import AIProvider
from app.ai.schemas import (
    CoverLetterGenerationRequest,
    ResumeGenerationRequest,
)

_CAPABILITIES = ProviderCapabilities(
    supports_cover_letters=True,
    supports_resume_generation=True,
    supports_streaming=False,
    supports_json_mode=False,
    supports_vision=False,
)


class OpenAIProvider(
    BaseChatProvider,
    AIProvider,
):
    """
    OpenAI implementation of the AIProvider interface.
    """

    def __init__(
        self,
        config: AISettings,
    ) -> None:
        self.config = config

        if not config.api_key:
            raise AIConfigurationError(
                "OPENAI_API_KEY is not configured.",
            )

        self.client = OpenAI(
            api_key=config.api_key,
            timeout=config.timeout,
        )

    @property
    def capabilities(
        self,
    ) -> ProviderCapabilities:
        return _CAPABILITIES

    def create_completion(
        self,
        *,
        messages: list[dict[str, str]],
    ):
        """
        Execute an OpenAI chat completion request.
        """

        return self.client.chat.completions.create(
            model=self.config.default_model,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            messages=messages,
        )

    @property
    def provider_name(
        self,
    ) -> str:
        """
        Return the provider identifier.
        """

        return "openai"

    @property
    def model_name(
        self,
    ) -> str:
        """
        Return the configured model.
        """

        return self.config.default_model

    @property
    def prompt_version(self) -> str:
        """
        Default prompt version exposed by this provider.
        """
        return self.config.resume_prompt_version

    def generate_cover_letter(
        self,
        request: CoverLetterGenerationRequest,
    ) -> AIExecutionResult[str]:
        """
        Generate a cover letter using OpenAI.
        """

        return self.execute_generation(
            messages=PromptService.build_cover_letter_messages(
                request,
                version=self.config.cover_letter_prompt_version,
            ),
            prompt_version=self.config.cover_letter_prompt_version,
            error_message="OpenAI failed to generate a cover letter.",
        )

    def generate_resume(
        self,
        request: ResumeGenerationRequest,
    ) -> AIExecutionResult[str]:
        """
        Generate a resume using OpenAI.
        """

        return self.execute_generation(
            messages=PromptService.build_resume_messages(
                request,
                version=self.config.resume_prompt_version,
            ),
            prompt_version=self.config.resume_prompt_version,
            error_message="OpenAI failed to generate a resume.",
        )
