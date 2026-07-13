from app.ai.prompts import CoverLetterPromptBuilder
from app.ai.schemas import (
    CoverLetterGenerationRequest,
)


def build_request():
    return CoverLetterGenerationRequest(
        company_name="OpenAI",
        job_title="Backend Engineer",
        job_description="Develop backend APIs.",
        resume_content="Five years of FastAPI experience.",
    )


def test_build_system_prompt():
    prompt = CoverLetterPromptBuilder.build_system_prompt()

    assert isinstance(prompt, str)
    assert "career coach" in prompt.lower()
    assert "cover letters" in prompt.lower()


def test_build_user_prompt_contains_resume():
    prompt = CoverLetterPromptBuilder.build_user_prompt(
        build_request(),
    )

    assert "Five years of FastAPI experience." in prompt


def test_build_user_prompt_contains_company():
    prompt = CoverLetterPromptBuilder.build_user_prompt(
        build_request(),
    )

    assert "OpenAI" in prompt


def test_build_user_prompt_contains_job_title():
    prompt = CoverLetterPromptBuilder.build_user_prompt(
        build_request(),
    )

    assert "Backend Engineer" in prompt


def test_build_user_prompt_contains_job_description():
    prompt = CoverLetterPromptBuilder.build_user_prompt(
        build_request(),
    )

    assert "Develop backend APIs." in prompt


def test_build_user_prompt_contains_instruction():
    prompt = CoverLetterPromptBuilder.build_user_prompt(
        build_request(),
    )

    assert "cover letter" in prompt.lower()
    assert "resume" in prompt.lower()
    assert "job description" in prompt.lower()
