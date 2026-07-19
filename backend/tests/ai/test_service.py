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
            content="Generated cover letter.",
            metadata=AIExecutionMetadata(
                provider="fake",
                model="fake-model",
                prompt_version="test-v1",
                prompt_tokens=100,
                completion_tokens=150,
                total_tokens=250,
                latency_ms=40,
                estimated_cost=0.0045,
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
                estimated_cost=0.00012,
            ),
        )


class FailingProvider(AIProvider):
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


def build_resume_request() -> ResumeGenerationRequest:
    return ResumeGenerationRequest(
        resume_content="Experienced FastAPI developer.",
    )


def build_retry_service() -> MagicMock:
    retry_service = MagicMock(spec=RetryService)

    def execute_side_effect(
        operation,
        *args,
        on_retry=None,
        **kwargs,
    ):
        return operation(*args, **kwargs)

    retry_service.execute.side_effect = execute_side_effect

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


def test_generate_resume_success():
    retry_service = build_retry_service()

    service = AIService(
        provider=SuccessfulProvider(),
        retry_service=retry_service,
    )

    response = service.generate_resume(
        build_resume_request(),
    )

    retry_service.execute.assert_called_once()

    assert response.content == "Generated resume."

    assert response.metadata.provider == "fake"
    assert response.metadata.model == "fake-model"
    assert response.metadata.prompt_version == "test-v1"
    assert response.metadata.prompt_tokens == 1
    assert response.metadata.completion_tokens == 1
    assert response.metadata.total_tokens == 2
    assert response.metadata.latency_ms == 1


def test_generate_resume_propagates_provider_exception():
    retry_service = build_retry_service()

    service = AIService(
        provider=FailingProvider(),
        retry_service=retry_service,
    )

    with pytest.raises(
        AIGenerationError,
        match="Generation failed.",
    ):
        service.generate_resume(
            build_resume_request(),
        )

    retry_service.execute.assert_called_once()


def test_generate_cover_letter_without_retry_service():
    service = AIService(
        provider=SuccessfulProvider(),
        retry_service=None,
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


def test_generate_resume_without_retry_service():
    service = AIService(
        provider=SuccessfulProvider(),
        retry_service=None,
    )

    response = service.generate_resume(
        build_resume_request(),
    )

    assert response.content == "Generated resume."

    assert response.metadata.provider == "fake"
    assert response.metadata.model == "fake-model"
    assert response.metadata.prompt_version == "test-v1"
    assert response.metadata.prompt_tokens == 1
    assert response.metadata.completion_tokens == 1
    assert response.metadata.total_tokens == 2
    assert response.metadata.latency_ms == 1


def test_generate_resume_emits_observability_success():
    observability = MagicMock()
    context = MagicMock()

    observability.execution_started.return_value = context

    provider = SuccessfulProvider()
    request = build_resume_request()

    service = AIService(
        provider=provider,
        observability_service=observability,
    )

    result = service.generate_resume(request)

    assert result.content == "Generated resume."

    observability.execution_started.assert_called_once_with(
        provider="openai",
        model="gpt-5",
        prompt_version="v1",
        operation="resume_generation",
        request_id=None,
        user_id=None,
        resume_id=None,
        cover_letter_id=None,
    )

    observability.execution_succeeded.assert_called_once_with(
        context,
    )

    observability.execution_failed.assert_not_called()


def test_generate_resume_emits_observability_failure():
    observability = MagicMock()
    context = MagicMock()

    observability.execution_started.return_value = context

    provider = FailingProvider()
    request = build_resume_request()

    service = AIService(
        provider=provider,
        observability_service=observability,
    )

    with pytest.raises(
        AIGenerationError,
        match="Generation failed.",
    ) as exc_info:
        service.generate_resume(request)

    observability.execution_started.assert_called_once_with(
        provider="openai",
        model="gpt-5",
        prompt_version="v1",
        operation="resume_generation",
        request_id=None,
        user_id=None,
        resume_id=None,
        cover_letter_id=None,
    )

    observability.execution_failed.assert_called_once_with(
        context,
        exc_info.value,
    )

    observability.execution_succeeded.assert_not_called()


def test_generate_resume_emits_retry_events():
    observability = MagicMock()

    context = MagicMock()

    observability.execution_started.return_value = context

    retry_service = MagicMock()

    provider = SuccessfulProvider()

    request = build_resume_request()

    def execute(
        operation,
        request,
        *,
        on_retry=None,
    ):
        on_retry(
            1,
            1.0,
        )

        return operation(
            request,
        )

    retry_service.execute.side_effect = execute

    service = AIService(
        provider=provider,
        retry_service=retry_service,
        observability_service=observability,
    )

    result = service.generate_resume(
        request,
    )

    assert result.content == "Generated resume."

    observability.execution_started.assert_called_once()

    observability.execution_retry.assert_called_once_with(
        context,
    )

    observability.execution_succeeded.assert_called_once_with(
        context,
    )

    observability.execution_failed.assert_not_called()


def test_generate_resume_without_observability():
    service = AIService(
        provider=SuccessfulProvider(),
    )

    result = service.generate_resume(
        build_resume_request(),
    )

    assert result.content == "Generated resume."


def test_generate_resume_attaches_usage_to_observability_context():
    observability = MagicMock()
    context = MagicMock()

    observability.execution_started.return_value = context

    service = AIService(
        provider=SuccessfulProvider(),
        observability_service=observability,
    )

    result = service.generate_resume(
        build_resume_request(),
    )

    assert result.content == "Generated resume."

    context.attach_usage.assert_called_once_with(
        prompt_tokens=1,
        completion_tokens=1,
        total_tokens=2,
        estimated_cost=0.00012,
    )

    observability.execution_succeeded.assert_called_once_with(
        context,
    )
