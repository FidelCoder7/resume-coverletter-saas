from app.ai.schemas import (
    CoverLetterGenerationRequest,
    ResumeGenerationRequest,
)


class CoverLetterPromptBuilder:
    """
    Builds prompts used for AI cover letter generation.
    """

    @staticmethod
    def build_system_prompt() -> str:
        """
        Return the system prompt.
        """

        return (
            "You are an expert career coach and professional resume writer. "
            "Write persuasive, truthful, ATS-friendly cover letters that are "
            "tailored to the supplied resume and job description. "
            "Do not invent qualifications or experience that are not present "
            "in the resume."
        )

    @staticmethod
    def build_user_prompt(
        request: CoverLetterGenerationRequest,
    ) -> str:
        """
        Build the user prompt.
        """

        return f"""
        Use the following resume and job description to write a professional
        cover letter.

        Resume

        {request.resume_content}

        Company

        {request.company_name}

        Job Title

        {request.job_title}

        Job Description

        {request.job_description}

        Requirements

        - Tailor the cover letter to the job.
        - Highlight relevant experience from the resume.
        - Keep a professional tone.
        - Do not invent qualifications.
        - Do not use placeholders.
        - Return only the cover letter.
        """.strip()


class ResumePromptBuilder:
    """
    Builds prompts used for AI resume generation.
    """

    @staticmethod
    def build_system_prompt() -> str:
        """
        Return the system prompt.
        """

        return (
            "You are an expert resume writer and ATS optimization specialist. "
            "Rewrite the supplied resume into a professional, ATS-friendly "
            "resume. Improve wording, grammar, readability, clarity, and "
            "professional impact while preserving factual accuracy. "
            "Do not invent experience, education, skills, certifications, "
            "dates, employers, achievements, or technologies that are not "
            "present in the supplied resume. Return only the completed resume."
        )

    @staticmethod
    def build_user_prompt(
        request: ResumeGenerationRequest,
    ) -> str:
        """
        Build the user prompt.
        """

        sections = [
            "Rewrite the following resume.",
            "",
            "Resume",
            "",
            request.resume_content,
        ]

        if request.target_job_title:
            sections.extend(
                [
                    "",
                    "Target Job Title",
                    "",
                    request.target_job_title,
                ]
            )

        if request.job_description:
            sections.extend(
                [
                    "",
                    "Job Description",
                    "",
                    request.job_description,
                ]
            )

        sections.extend(
            [
                "",
                "Requirements",
                "",
                "- Improve wording and grammar.",
                "- Improve ATS compatibility.",
                "- Preserve all factual information.",
                "- Do not invent qualifications or experience.",
                "- Return only the completed resume.",
            ]
        )

        return "\n".join(sections)
