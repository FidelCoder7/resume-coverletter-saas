from openai import (
    APITimeoutError,
    OpenAI,
    OpenAIError,
    RateLimitError,
)

from app.ai.exceptions import (
    AIConfigurationError,
    AIGenerationError,
    AIProviderError,
    AIRateLimitError,
    AITimeoutError,
)
from app.ai.prompts import CoverLetterPromptBuilder
from app.ai.providers import AIProvider
from app.ai.schemas import (
    CoverLetterGenerationRequest,
    CoverLetterGenerationResponse,
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

    @staticmethod
    def _build_messages(
        request: CoverLetterGenerationRequest,
    ) -> list[dict[str, str]]:
        """
        Build the OpenAI chat messages.
        """

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

    def generate_cover_letter(
        self,
        request: CoverLetterGenerationRequest,
    ) -> CoverLetterGenerationResponse:
        """
        Generate a cover letter using OpenAI.
        """

        try:
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                temperature=settings.OPENAI_TEMPERATURE,
                max_tokens=settings.OPENAI_MAX_TOKENS,
                messages=self._build_messages(
                    request,
                ),
            )

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

            return CoverLetterGenerationResponse(
                content=content,
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
                "OpenAI failed to generate a cover letter.",
            ) from exc
