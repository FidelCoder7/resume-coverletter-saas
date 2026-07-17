from unittest.mock import MagicMock

import pytest

from app.ai.contracts import (
    AIExecutionMetadata,
    AIExecutionResult,
)
from app.ai.exceptions import AIGenerationError
from app.ai.provider_capabilities import ProviderCapabilities
from app.ai.providers import AIProvider
from app.ai.retry import RetryService
from app.ai.schemas import (
    CoverLetterGenerationRequest,
    ResumeGenerationRequest,
)
from app.ai.service import AIService

_CAPABILITIES = ProviderCapabilities()


class SuccessfulProvider(AIProvider):
    @property
    def capabilities(
        self,
    ) -> ProviderCapabilities:
        return _CAPABILITIES

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
            content="Generated resume.",
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
    @property
    def capabilities(
        self,
    ) -> ProviderCapabilities:
        return _CAPABILITIES

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
        raise AIGenerationError(
            "Generation failed.",
        )


def build_request() -> CoverLetterGenerationRequest:
    return CoverLetterGenerationRequest(
        company_name="OpenAI",
        job_title="Backend Engineer",
        job_description="Looking for a Python backend engineer.",
        resume_content="Experienced FastAPI developer.",
    )


def build_retry_service() -> MagicMock:
    retry_service = MagicMock(
        spec=RetryService,
    )

    retry_service.execute.side_effect = lambda func, *args, **kwargs: func(
        *args, **kwargs
    )

    return retry_service


def test_generate_cover_letter_success():
    retry_service = build_retry_service()

    service = AIService(
        provider=SuccessfulProvider(),
        retry_service=retry_service,
    )

    response = service.generate_cover_letter(
        build_request(),
    )

    retry_service.execute.assert_called_once()

    assert response.content == "Generated cover letter."

    assert response.metadata.provider == "fake"
    assert response.metadata.model == "fake-model"
    assert response.metadata.prompt_version == "test-v1"
    assert response.metadata.prompt_tokens == 100
    assert response.metadata.completion_tokens == 150
    assert response.metadata.total_tokens == 250
    assert response.metadata.latency_ms == 40


def test_generate_cover_letter_propagates_provider_exception():
    retry_service = build_retry_service()

    service = AIService(
        provider=FailingProvider(),
        retry_service=retry_service,
    )

    with pytest.raises(
        AIGenerationError,
        match="Generation failed.",
    ):
        service.generate_cover_letter(
            build_request(),
        )

    retry_service.execute.assert_called_once()
