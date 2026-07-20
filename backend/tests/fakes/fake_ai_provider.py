from app.ai.contracts import (
    AIExecutionMetadata,
    AIExecutionResult,
)
from app.ai.provider_capabilities import ProviderCapabilities
from app.ai.providers import AIProvider
from app.ai.schemas import (
    ATSOptimizationRequest,
    CoverLetterGenerationRequest,
    ResumeGenerationRequest,
)

_CAPABILITIES = ProviderCapabilities(
    supports_cover_letters=True,
    supports_resume_generation=True,
    supports_ats_optimization=True,
)

_PROVIDER = "fake"
_MODEL = "fake-model"
_PROMPT_VERSION = "test-v1"

GENERATED_COVER_LETTER = "This is a generated cover letter for testing purposes."

GENERATED_RESUME = (
    "Professional Python Backend Engineer\n\n"
    "Experienced FastAPI developer with strong API design skills."
)

GENERATED_ATS_OPTIMIZATION = """
{
  "overall_score": 88,
  "summary": "Resume optimized successfully.",
  "optimized_resume": "Optimized ATS-friendly resume content.",
  "strengths": [
    "Strong technical skills",
    "Clear work history"
  ],
  "weaknesses": [
    "Needs more measurable achievements"
  ],
  "missing_keywords": [
    "Docker",
    "CI/CD"
  ]
}
""".strip()


class FakeAIProvider(AIProvider):
    """
    Fake AI provider used by service tests.
    """

    @property
    def capabilities(
        self,
    ) -> ProviderCapabilities:
        return _CAPABILITIES

    @property
    def provider_name(
        self,
    ) -> str:
        return _PROVIDER

    @property
    def model_name(
        self,
    ) -> str:
        return _MODEL

    @property
    def prompt_version(
        self,
    ) -> str:
        return _PROMPT_VERSION

    @staticmethod
    def _metadata() -> AIExecutionMetadata:
        return AIExecutionMetadata(
            provider=_PROVIDER,
            model=_MODEL,
            prompt_version=_PROMPT_VERSION,
            prompt_tokens=120,
            completion_tokens=240,
            total_tokens=360,
            latency_ms=45,
        )

    def generate_cover_letter(
        self,
        request: CoverLetterGenerationRequest,
    ) -> AIExecutionResult[str]:
        return AIExecutionResult(
            content=GENERATED_COVER_LETTER,
            metadata=self._metadata(),
        )

    def generate_resume(
        self,
        request: ResumeGenerationRequest,
    ) -> AIExecutionResult[str]:
        return AIExecutionResult(
            content=GENERATED_RESUME,
            metadata=self._metadata(),
        )

    def generate_ats_optimization(
        self,
        request: ATSOptimizationRequest,
    ) -> AIExecutionResult[str]:
        return AIExecutionResult(
            content=GENERATED_ATS_OPTIMIZATION,
            metadata=self._metadata(),
        )
