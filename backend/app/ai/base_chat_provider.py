from abc import ABC, abstractmethod
from time import perf_counter

from openai import (
    APITimeoutError,
    OpenAIError,
    RateLimitError,
)

from app.ai.contracts import (
    AIExecutionMetadata,
    AIExecutionResult,
)
from app.ai.exceptions import (
    AIGenerationError,
    AIProviderError,
    AIRateLimitError,
    AITimeoutError,
)


class BaseChatProvider(ABC):
    """
    Base implementation shared by chat-completion providers.
    """

    @abstractmethod
    def create_completion(
        self,
        *,
        messages: list[dict[str, str]],
    ):
        """
        Execute the provider-specific completion request.
        """

    @property
    @abstractmethod
    def provider_name(
        self,
    ) -> str:
        """
        Return the provider identifier.
        """

    @property
    @abstractmethod
    def model_name(
        self,
    ) -> str:
        """
        Return the configured model.
        """

    def execute_generation(
        self,
        *,
        messages: list[dict[str, str]],
        prompt_version: str,
        error_message: str,
    ) -> AIExecutionResult[str]:
        """
        Execute a chat completion request.

        Successful executions return both generated content and
        execution metadata.

        Failed executions raise an AI exception carrying the
        metadata available at the time of failure.
        """

        start = perf_counter()

        def build_metadata(
            *,
            prompt_tokens: int | None = None,
            completion_tokens: int | None = None,
            total_tokens: int | None = None,
        ) -> AIExecutionMetadata:
            return AIExecutionMetadata(
                provider=self.provider_name,
                model=self.model_name,
                prompt_version=prompt_version,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=total_tokens,
                latency_ms=int(
                    (perf_counter() - start) * 1000,
                ),
            )

        try:
            response = self.create_completion(
                messages=messages,
            )

            usage = response.usage

            metadata = build_metadata(
                prompt_tokens=(usage.prompt_tokens if usage else None),
                completion_tokens=(usage.completion_tokens if usage else None),
                total_tokens=(usage.total_tokens if usage else None),
            )

            if not response.choices:
                raise AIGenerationError(
                    "The AI provider returned no choices.",
                    metadata=metadata,
                )

            choice = response.choices[0]

            if choice.finish_reason == "length":
                raise AIGenerationError(
                    "The AI response exceeded the configured token limit.",
                    metadata=metadata,
                )

            message = choice.message

            if message is None or message.content is None:
                raise AIGenerationError(
                    "The AI provider returned an empty response.",
                    metadata=metadata,
                )

            content = message.content.strip()

            if not content:
                raise AIGenerationError(
                    "The AI provider returned an empty response.",
                    metadata=metadata,
                )

            return AIExecutionResult(
                content=content,
                metadata=metadata,
            )

        except APITimeoutError as exc:
            raise AITimeoutError(
                "The AI request timed out.",
                metadata=build_metadata(),
            ) from exc

        except RateLimitError as exc:
            raise AIRateLimitError(
                "The AI provider rate limit has been exceeded.",
                metadata=build_metadata(),
            ) from exc

        except OpenAIError as exc:
            raise AIProviderError(
                error_message,
                metadata=build_metadata(),
            ) from exc
