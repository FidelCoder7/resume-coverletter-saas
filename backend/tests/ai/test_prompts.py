from app.ai.prompts import (
    ATSOptimizationPromptBuilder,
    CoverLetterPromptBuilder,
    ResumePromptBuilder,
)
from app.ai.schemas import (
    ATSOptimizationRequest,
    CoverLetterGenerationRequest,
    ResumeGenerationRequest,
)


def build_cover_letter_request() -> CoverLetterGenerationRequest:
    return CoverLetterGenerationRequest(
        company_name="OpenAI",
        job_title="Backend Engineer",
        job_description="Develop backend APIs.",
        resume_content="Five years of FastAPI experience.",
    )


def build_resume_request() -> ResumeGenerationRequest:
    return ResumeGenerationRequest(
        resume_content="Five years of FastAPI experience.",
        target_job_title="Backend Engineer",
        job_description="Develop backend APIs.",
    )


def build_ats_request() -> ATSOptimizationRequest:
    return ATSOptimizationRequest(
        resume_content=(
            "Five years of FastAPI experience building REST APIs "
            "with PostgreSQL and Docker."
        ),
        job_description=(
            "Seeking a Backend Engineer with FastAPI, Docker, "
            "PostgreSQL, CI/CD and cloud deployment experience."
        ),
    )


#
# Cover Letter Prompt Builder
#


def test_cover_letter_system_prompt():
    prompt = CoverLetterPromptBuilder.build_system_prompt()

    assert isinstance(prompt, str)
    assert "career coach" in prompt.lower()
    assert "cover letters" in prompt.lower()


def test_cover_letter_user_prompt_contains_resume():
    prompt = CoverLetterPromptBuilder.build_user_prompt(
        build_cover_letter_request(),
    )

    assert "Five years of FastAPI experience." in prompt


def test_cover_letter_user_prompt_contains_company():
    prompt = CoverLetterPromptBuilder.build_user_prompt(
        build_cover_letter_request(),
    )

    assert "OpenAI" in prompt


def test_cover_letter_user_prompt_contains_job_title():
    prompt = CoverLetterPromptBuilder.build_user_prompt(
        build_cover_letter_request(),
    )

    assert "Backend Engineer" in prompt


def test_cover_letter_user_prompt_contains_job_description():
    prompt = CoverLetterPromptBuilder.build_user_prompt(
        build_cover_letter_request(),
    )

    assert "Develop backend APIs." in prompt


def test_cover_letter_user_prompt_contains_instruction():
    prompt = CoverLetterPromptBuilder.build_user_prompt(
        build_cover_letter_request(),
    )

    assert "cover letter" in prompt.lower()
    assert "resume" in prompt.lower()
    assert "job description" in prompt.lower()


#
# Resume Prompt Builder
#


def test_resume_system_prompt():
    prompt = ResumePromptBuilder.build_system_prompt()

    assert isinstance(prompt, str)
    assert "resume writer" in prompt.lower()
    assert "ats" in prompt.lower()


def test_resume_user_prompt_contains_resume():
    prompt = ResumePromptBuilder.build_user_prompt(
        build_resume_request(),
    )

    assert "Five years of FastAPI experience." in prompt


def test_resume_user_prompt_contains_target_job():
    prompt = ResumePromptBuilder.build_user_prompt(
        build_resume_request(),
    )

    assert "Backend Engineer" in prompt


def test_resume_user_prompt_contains_job_description():
    prompt = ResumePromptBuilder.build_user_prompt(
        build_resume_request(),
    )

    assert "Develop backend APIs." in prompt


def test_resume_user_prompt_contains_requirements():
    prompt = ResumePromptBuilder.build_user_prompt(
        build_resume_request(),
    )

    assert "Improve ATS compatibility." in prompt
    assert "Return only the completed resume." in prompt


#
# ATS Optimization Prompt Builder
#


def test_ats_system_prompt():
    prompt = ATSOptimizationPromptBuilder.build_system_prompt()

    assert isinstance(prompt, str)
    assert "ats" in prompt.lower()
    assert "json" in prompt.lower()
    assert "resume" in prompt.lower()


def test_ats_user_prompt_contains_resume():
    prompt = ATSOptimizationPromptBuilder.build_user_prompt(
        build_ats_request(),
    )

    assert "Five years of FastAPI experience" in prompt


def test_ats_user_prompt_contains_job_description():
    prompt = ATSOptimizationPromptBuilder.build_user_prompt(
        build_ats_request(),
    )

    assert "Backend Engineer" in prompt
    assert "CI/CD" in prompt


def test_ats_user_prompt_requests_json():
    prompt = ATSOptimizationPromptBuilder.build_user_prompt(
        build_ats_request(),
    )

    assert "json" in prompt.lower()


def test_ats_user_prompt_mentions_keyword_analysis():
    prompt = ATSOptimizationPromptBuilder.build_user_prompt(
        build_ats_request(),
    )

    assert "keyword" in prompt.lower()


def test_ats_user_prompt_mentions_optimized_resume():
    prompt = ATSOptimizationPromptBuilder.build_user_prompt(
        build_ats_request(),
    )

    assert "optimized resume" in prompt.lower()
