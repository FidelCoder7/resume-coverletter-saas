from app.ai.schemas import CoverLetterGenerationRequest


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
