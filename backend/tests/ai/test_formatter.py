from datetime import date

from app.ai.formatters import ResumeFormatter
from app.certifications.models import Certification
from app.common.constants import EmploymentType, SkillLevel
from app.educations.models import Education
from app.experiences.models import Experience
from app.projects.models import Project
from app.skills.models import Skill
from tests.factories.resume_factory import make_resume


def test_format_empty_resume():
    resume = make_resume(
        user_id=None,
        title="Backend Resume",
        summary=None,
    )

    resume.skills = []
    resume.experiences = []
    resume.educations = []
    resume.projects = []
    resume.certifications = []

    output = ResumeFormatter.format(resume)

    assert "Resume Title: Backend Resume" in output
    assert "Professional Summary" not in output
    assert "Skills" not in output
    assert "Experience" not in output
    assert "Education" not in output
    assert "Projects" not in output
    assert "Certifications" not in output


def test_format_summary():
    resume = make_resume(
        user_id=None,
        summary="Experienced Python developer.",
    )

    resume.skills = []
    resume.experiences = []
    resume.educations = []
    resume.projects = []
    resume.certifications = []

    output = ResumeFormatter.format(resume)

    assert "Professional Summary" in output
    assert "Experienced Python developer." in output


def test_format_skills():
    resume = make_resume(
        user_id=None,
    )

    resume.skills = [
        Skill(
            name="Python",
            proficiency=SkillLevel.EXPERT,
        ),
        Skill(
            name="FastAPI",
            proficiency=SkillLevel.ADVANCED,
        ),
    ]

    resume.experiences = []
    resume.educations = []
    resume.projects = []
    resume.certifications = []

    output = ResumeFormatter.format(resume)

    assert "Skills" in output
    assert "Python" in output
    assert SkillLevel.EXPERT in output
    assert "FastAPI" in output
    assert SkillLevel.ADVANCED.value in output


def test_format_experience():
    resume = make_resume(
        user_id=None,
    )

    resume.skills = []

    resume.experiences = [
        Experience(
            company="OpenAI",
            job_title="Backend Engineer",
            employment_type=EmploymentType.FULL_TIME,
            start_date=date(2023, 1, 1),
            is_current=True,
            display_order=0,
            description="Built APIs using FastAPI.",
        ),
    ]

    resume.educations = []
    resume.projects = []
    resume.certifications = []

    output = ResumeFormatter.format(resume)

    assert "Experience" in output
    assert "OpenAI" in output
    assert "Backend Engineer" in output
    assert "Built APIs using FastAPI." in output


def test_format_education():
    resume = make_resume(
        user_id=None,
    )

    resume.skills = []
    resume.experiences = []

    resume.educations = [
        Education(
            degree="BSc Computer Science",
            institution="University",
        ),
    ]

    resume.projects = []
    resume.certifications = []

    output = ResumeFormatter.format(resume)

    assert "Education" in output
    assert "BSc Computer Science" in output
    assert "University" in output


def test_format_projects():
    resume = make_resume(
        user_id=None,
    )

    resume.skills = []
    resume.experiences = []
    resume.educations = []

    resume.projects = [
        Project(
            name="Resume SaaS",
            description="Full-stack SaaS project.",
        ),
    ]

    resume.certifications = []

    output = ResumeFormatter.format(resume)

    assert "Projects" in output
    assert "Resume SaaS" in output
    assert "Full-stack SaaS project." in output


def test_format_certifications():
    resume = make_resume(
        user_id=None,
    )

    resume.skills = []
    resume.experiences = []
    resume.educations = []
    resume.projects = []

    resume.certifications = [
        Certification(
            name="AWS Certified Developer",
        ),
    ]

    output = ResumeFormatter.format(resume)

    assert "Certifications" in output
    assert "AWS Certified Developer" in output


def test_format_complete_resume():
    resume = make_resume(
        user_id=None,
        title="Senior Backend Resume",
        summary="Senior Python engineer.",
    )

    resume.skills = [
        Skill(
            name="Python",
            proficiency=SkillLevel.EXPERT,
        ),
    ]

    resume.experiences = [
        Experience(
            company="OpenAI",
            job_title="Backend Engineer",
            employment_type=EmploymentType.FULL_TIME,
            start_date=date(2023, 1, 1),
            is_current=True,
            display_order=0,
            description="Built scalable APIs.",
        ),
    ]

    resume.educations = [
        Education(
            degree="BSc Computer Science",
            institution="University",
        ),
    ]

    resume.projects = [
        Project(
            name="Resume SaaS",
            description="AI-powered application.",
        ),
    ]

    resume.certifications = [
        Certification(
            name="AWS Developer",
        ),
    ]

    output = ResumeFormatter.format(resume)

    assert "Senior Backend Resume" in output
    assert "Senior Python engineer." in output
    assert "Python" in output
    assert "OpenAI" in output
    assert "Backend Engineer" in output
    assert "University" in output
    assert "Resume SaaS" in output
    assert "AWS Developer" in output
