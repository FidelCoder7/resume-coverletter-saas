from time import perf_counter

from openai import (
    APITimeoutError,
    OpenAI,
    OpenAIError,
    RateLimitError,
)

from app.ai.contracts import (
    AIExecutionMetadata,
    AIExecutionResult,
)
from app.ai.exceptions import (
    AIConfigurationError,
    AIGenerationError,
    AIProviderError,
    AIRateLimitError,
    AITimeoutError,
)
from app.ai.prompts import (
    CoverLetterPromptBuilder,
    ResumePromptBuilder,
)
from app.ai.providers import AIProvider
from app.ai.schemas import (
    CoverLetterGenerationRequest,
    ResumeGenerationRequest,
)
from app.core.config import settings


class OpenAIProvider(AIProvider):
    """
    OpenAI implementation of the AIProvider interface.
    """

    def __init__(self) -> None:
        api_key = settings.OPENAI_API_KEY

        if not api_key:
            raise AIConfigurationError(
                "OPENAI_API_KEY is not configured.",
            )

        self.client = OpenAI(
            api_key=api_key,
            timeout=settings.OPENAI_TIMEOUT,
        )

    def _execute_generation(
        self,
        *,
        messages: list[dict[str, str]],
        prompt_version: str,
        error_message: str,
    ) -> AIExecutionResult[str]:
        """
        Execute a chat completion request.
        """

        try:
            start = perf_counter()

            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                temperature=settings.OPENAI_TEMPERATURE,
                max_tokens=settings.OPENAI_MAX_TOKENS,
                messages=messages,
            )

            latency_ms = int((perf_counter() - start) * 1000)

            if not response.choices:
                raise AIGenerationError(
                    "The AI provider returned no choices.",
                )

            choice = response.choices[0]

            if choice.finish_reason == "length":
                raise AIGenerationError(
                    "The AI response exceeded the configured token limit.",
                )

            message = choice.message

            if message is None or message.content is None:
                raise AIGenerationError(
                    "The AI provider returned an empty response.",
                )

            content = message.content.strip()

            if not content:
                raise AIGenerationError(
                    "The AI provider returned an empty response.",
                )

            usage = response.usage

            return AIExecutionResult(
                content=content,
                metadata=AIExecutionMetadata(
                    provider="openai",
                    model=settings.OPENAI_MODEL,
                    prompt_version=prompt_version,
                    prompt_tokens=usage.prompt_tokens if usage else None,
                    completion_tokens=usage.completion_tokens if usage else None,
                    total_tokens=usage.total_tokens if usage else None,
                    latency_ms=latency_ms,
                ),
            )

        except APITimeoutError as exc:
            raise AITimeoutError(
                "The AI request timed out.",
            ) from exc

        except RateLimitError as exc:
            raise AIRateLimitError(
                "The AI provider rate limit has been exceeded.",
            ) from exc

        except OpenAIError as exc:
            raise AIProviderError(
                error_message,
            ) from exc

    @staticmethod
    def _build_cover_letter_messages(
        request: CoverLetterGenerationRequest,
    ) -> list[dict[str, str]]:
        return [
            {
                "role": "system",
                "content": (CoverLetterPromptBuilder.build_system_prompt()),
            },
            {
                "role": "user",
                "content": (
                    CoverLetterPromptBuilder.build_user_prompt(
                        request,
                    )
                ),
            },
        ]

    @staticmethod
    def _build_resume_messages(
        request: ResumeGenerationRequest,
    ) -> list[dict[str, str]]:
        return [
            {
                "role": "system",
                "content": (ResumePromptBuilder.build_system_prompt()),
            },
            {
                "role": "user",
                "content": (
                    ResumePromptBuilder.build_user_prompt(
                        request,
                    )
                ),
            },
        ]

    def generate_cover_letter(
        self,
        request: CoverLetterGenerationRequest,
    ) -> AIExecutionResult[str]:
        """
        Generate a cover letter using OpenAI.
        """

        return self._execute_generation(
            messages=self._build_cover_letter_messages(
                request,
            ),
            prompt_version="cover_letter_v1",
            error_message="OpenAI failed to generate a cover letter.",
        )

    def generate_resume(
        self,
        request: ResumeGenerationRequest,
    ) -> AIExecutionResult[str]:
        """
        Generate a resume using OpenAI.
        """

        return self._execute_generation(
            messages=self._build_resume_messages(
                request,
            ),
            prompt_version="resume_v1",
            error_message="OpenAI failed to generate a resume.",
        )
