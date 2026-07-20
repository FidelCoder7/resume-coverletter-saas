from app.ai.schemas import (
    ATSOptimizationRequest,
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


class ATSOptimizationPromptBuilder:
    """
    Builds prompts dedicated to ATS resume optimization.

    Unlike ResumePromptBuilder, this builder assumes that an existing
    resume already exists and focuses on maximizing compatibility with
    a specific job description while preserving factual accuracy.
    """

    @staticmethod
    def build_system_prompt() -> str:
        """
        Return the ATS optimization system prompt.
        """

        return (
            "You are an expert ATS optimization specialist, technical recruiter, "
            "and professional resume writer. Your responsibility is to optimize "
            "an existing resume for Applicant Tracking Systems while remaining "
            "completely truthful. Improve keyword alignment, section clarity, "
            "professional wording, readability, and ATS compatibility. Never "
            "invent employers, education, dates, certifications, technologies, "
            "projects, responsibilities, or achievements that are not supported "
            "by the supplied resume. "
            "Return your response as valid JSON only."
        )

    @staticmethod
    def build_user_prompt(
        request: ATSOptimizationRequest,
    ) -> str:
        """
        Build the ATS optimization prompt.
        """

        sections = [
            "Optimize the following resume for the supplied job description.",
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

        sections.extend(
            [
                "",
                "Job Description",
                "",
                request.job_description,
                "",
                "Requirements",
                "",
                "- Preserve all factual information.",
                "- Improve ATS keyword alignment.",
                "- Improve professional wording.",
                "- Improve readability.",
                "- Improve action-oriented language.",
                "- Improve measurable impact where evidence already exists.",
                "- Do not invent qualifications.",
                "- Do not invent experience.",
                "- Do not invent achievements.",
                "",
                "Return ONLY valid JSON.",
                "",
                "The optimized resume must be returned as structured JSON.",
                "",
                "The JSON must contain these fields:",
                '- "optimized_resume": string',
                '- "ats_score": integer between 0 and 100',
                '- "missing_keywords": array of strings',
                '- "matched_keywords": array of strings',
                '- "recommendations": array of strings',
            ]
        )

        return "\n".join(sections)
