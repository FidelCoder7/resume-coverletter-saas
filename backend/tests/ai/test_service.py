import pytest

from app.ai.contracts import (
    AIExecutionMetadata,
    AIExecutionResult,
)
from app.ai.exceptions import AIGenerationError
from app.ai.providers import AIProvider
from app.ai.schemas import (
    CoverLetterGenerationRequest,
    ResumeGenerationRequest,
)
from app.ai.service import AIService


class SuccessfulProvider(AIProvider):
    def generate_cover_letter(
        self,
        request: CoverLetterGenerationRequest,
    ) -> AIExecutionResult[str]:
        return AIExecutionResult(
            content="Generated cover letter.",
            metadata=AIExecutionMetadata(
                provider="fake",
                model="fake-model",
                prompt_version="test-v1",
                prompt_tokens=100,
                completion_tokens=150,
                total_tokens=250,
                latency_ms=40,
            ),
        )
    
    def generate_resume(
        self,
        request: ResumeGenerationRequest,
    ) -> AIExecutionResult[str]:
        return AIExecutionResult(
            content="Generated resume",
            metadata=AIExecutionMetadata(
                provider="fake",
                model="fake-model",
                prompt_version="test-v1",
                prompt_tokens=1,
                completion_tokens=1,
                total_tokens=2,
                latency_ms=1,
            ),
        )


class FailingProvider(AIProvider):
    def generate_cover_letter(
        self,
        request: CoverLetterGenerationRequest,
    ) -> AIExecutionResult[str]:
        raise AIGenerationError(
            "Generation failed.",
        )
    
    def generate_resume(
        self,
        request: ResumeGenerationRequest,
    ) -> AIExecutionResult[str]:
        raise NotImplementedError


def build_request() -> CoverLetterGenerationRequest:
    return CoverLetterGenerationRequest(
        company_name="OpenAI",
        job_title="Backend Engineer",
        job_description="Looking for a Python backend engineer.",
        resume_content="Experienced FastAPI developer.",
    )


def test_generate_cover_letter_success():
    service = AIService(
        provider=SuccessfulProvider(),
    )

    response = service.generate_cover_letter(
        build_request(),
    )

    assert response.content == "Generated cover letter."

    assert response.metadata.provider == "fake"
    assert response.metadata.model == "fake-model"
    assert response.metadata.prompt_version == "test-v1"
    assert response.metadata.prompt_tokens == 100
    assert response.metadata.completion_tokens == 150
    assert response.metadata.total_tokens == 250
    assert response.metadata.latency_ms == 40


def test_generate_cover_letter_propagates_provider_exception():
    service = AIService(
        provider=FailingProvider(),
    )

    with pytest.raises(
        AIGenerationError,
        match="Generation failed.",
    ):
        service.generate_cover_letter(
            build_request(),
        )
