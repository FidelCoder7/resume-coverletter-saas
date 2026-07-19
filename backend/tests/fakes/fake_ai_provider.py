from app.ai.contracts import (
    AIExecutionMetadata,
    AIExecutionResult,
)
from app.ai.provider_capabilities import ProviderCapabilities
from app.ai.providers import AIProvider
from app.ai.schemas import CoverLetterGenerationRequest, ResumeGenerationRequest

_CAPABILITIES = ProviderCapabilities()
_PROVIDER = "fake"
_MODEL = "fake-model"
_PROMPT_VERSION = "test-v1"

GENERATED_COVER_LETTER = "This is a generated cover letter for testing purposes."

GENERATED_RESUME = (
    "Professional Python Backend Engineer\n\n"
    "Experienced FastAPI developer with strong API design skills."
)


class FakeAIProvider(AIProvider):
    """
    Fake AI provider used by service tests.
    """

    def _metadata(
        *,
        prompt_tokens: int,
        completion_tokens: int,
        total_tokens: int,
        latency_ms: int,
    ) -> AIExecutionMetadata:
        return AIExecutionMetadata(
            provider=_PROVIDER,
            model=_MODEL,
            prompt_version=_PROMPT_VERSION,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            latency_ms=latency_ms,
        )

    @property
    def capabilities(
        self,
    ) -> ProviderCapabilities:
        return _CAPABILITIES

    @property
    def provider_name(self) -> str:
        return "openai"

    @property
    def model_name(self) -> str:
        return "gpt-5"

    @property
    def prompt_version(self) -> str:
        return "v1"

    def generate_cover_letter(
        self,
        request: CoverLetterGenerationRequest,
    ) -> AIExecutionResult[str]:
        return AIExecutionResult(
            content=GENERATED_COVER_LETTER,
            metadata=AIExecutionMetadata(
                provider="fake",
                model="fake-model",
                prompt_version="test_v1",
                prompt_tokens=120,
                completion_tokens=240,
                total_tokens=360,
                latency_ms=40,
            ),
        )

    def generate_resume(
        self,
        request: ResumeGenerationRequest,
    ) -> AIExecutionResult[str]:
        return AIExecutionResult(
            content=GENERATED_RESUME,
            metadata=AIExecutionMetadata(
                provider="fake",
                model="fake-model",
                prompt_version="test-v1",
                prompt_tokens=120,
                completion_tokens=180,
                total_tokens=300,
                latency_ms=45,
            ),
        )
