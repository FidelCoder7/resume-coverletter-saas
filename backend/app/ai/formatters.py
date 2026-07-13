from app.resumes.models import Resume


class ResumeFormatter:
    """
    Formats a resume into plain text for AI prompt generation.
    """

    @staticmethod
    def format(
        resume: Resume,
    ) -> str:
        """
        Convert a Resume model into a structured plain-text
        representation suitable for AI prompts.
        """

        sections: list[str] = []

        sections.append(f"Resume Title: {resume.title}")

        if resume.summary:
            sections.extend(
                [
                    "",
                    "Professional Summary",
                    resume.summary,
                ],
            )

        if resume.skills:
            sections.extend(
                [
                    "",
                    "Skills",
                ],
            )

            for skill in resume.skills:
                sections.append(
                    f"- {skill.name} ({skill.proficiency.value})",
                )

        if resume.experiences:
            sections.extend(
                [
                    "",
                    "Experience",
                ],
            )

            for experience in resume.experiences:
                sections.append(
                    f"- {experience.job_title} | "
                    f"{experience.company} | "
                    f"{experience.employment_type.value}"
                )

                if experience.description:
                    sections.append(
                        f"  {experience.description}",
                    )

        if resume.educations:
            sections.extend(
                [
                    "",
                    "Education",
                ],
            )

            for education in resume.educations:
                sections.append(f"- {education.degree} - " f"{education.institution}")

        if resume.projects:
            sections.extend(
                [
                    "",
                    "Projects",
                ],
            )

            for project in resume.projects:
                sections.append(f"- {project.name}")

                if project.description:
                    sections.append(
                        f"  {project.description}",
                    )

        if resume.certifications:
            sections.extend(
                [
                    "",
                    "Certifications",
                ],
            )

            for certification in resume.certifications:
                sections.append(f"- {certification.name}")

        return "\n".join(sections).strip()
