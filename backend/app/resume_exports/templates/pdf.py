from html import escape

from app.resumes.models import Resume


def render_resume_html(
    resume: Resume,
) -> str:
    """
    Render a complete resume into self-contained HTML.

    The generated HTML is designed to be consumed by the PDF renderer.
    """

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{escape(resume.title)}</title>

    <style>
        @page {{
            size: A4;
            margin: 18mm 16mm 18mm 16mm;
        }}

        * {{
            box-sizing: border-box;
        }}

        body {{
            font-family: Arial, Helvetica, sans-serif;
            color: #222;
            font-size: 10.5pt;
            line-height: 1.45;
            margin: 0;
        }}

        h1,
        h2,
        h3,
        p {{
            margin-top: 0;
        }}

        h1 {{
            font-size: 24pt;
            margin-bottom: 4px;
        }}

        h2 {{
            font-size: 13pt;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            border-bottom: 1px solid #333;
            padding-bottom: 4px;
            margin-top: 18px;
            margin-bottom: 10px;
        }}

        h3 {{
            font-size: 11.5pt;
            margin-bottom: 2px;
        }}

        .header {{
            margin-bottom: 14px;
        }}

        .summary {{
            margin-bottom: 10px;
        }}

        .section {{
            page-break-inside: avoid;
        }}

        .entry {{
            margin-bottom: 12px;
            page-break-inside: avoid;
        }}

        .meta {{
            font-size: 9.5pt;
            color: #555;
            margin-bottom: 4px;
        }}

        .description {{
            white-space: pre-line;
        }}

        .skills {{
            display: block;
        }}

        .skill {{
            display: inline-block;
            margin-right: 8px;
            margin-bottom: 4px;
        }}

        .dates {{
            float: right;
        }}

        ul {{
            margin-top: 4px;
            padding-left: 18px;
        }}

        a {{
            color: #222;
            text-decoration: none;
        }}
    </style>
</head>

<body>

    <header class="header">
        <h1>{escape(resume.title)}</h1>
    </header>

    {render_summary(resume)}

    {render_experiences(resume)}

    {render_education(resume)}

    {render_skills(resume)}

    {render_projects(resume)}

    {render_certifications(resume)}

</body>
</html>
"""


def render_summary(
    resume: Resume,
) -> str:
    if not resume.summary:
        return ""

    return f"""
<section class="section">
    <h2>Professional Summary</h2>
    <p class="summary">
        {escape(resume.summary)}
    </p>
</section>
"""


def render_experiences(
    resume: Resume,
) -> str:
    if not resume.experiences:
        return ""

    entries = []

    for experience in resume.experiences:
        start_date = experience.start_date.strftime("%b %Y")

        if experience.is_current:
            end_date = "Present"
        elif experience.end_date:
            end_date = experience.end_date.strftime("%b %Y")
        else:
            end_date = ""

        dates = f"{start_date} - {end_date}"

        description = ""

        if experience.description:
            description = f"""
            <p class="description">
                {escape(experience.description)}
            </p>
            """

        entries.append(f"""
            <article class="entry">
                <h3>
                    {escape(experience.job_title)}
                </h3>

                <div class="meta">
                    {escape(experience.company)}
                    {" | " + escape(experience.location)
                    if experience.location else ""}
                    <span class="dates">
                        {escape(dates)}
                    </span>
                </div>

                {description}
            </article>
            """)

    return f"""
<section class="section">
    <h2>Experience</h2>
    {"".join(entries)}
</section>
"""


def render_education(
    resume: Resume,
) -> str:
    if not resume.educations:
        return ""

    entries = []

    for education in resume.educations:
        start_date = education.start_date.strftime("%Y")

        if education.is_current:
            end_date = "Present"
        elif education.end_date:
            end_date = education.end_date.strftime("%Y")
        else:
            end_date = ""

        dates = f"{start_date} - {end_date}"

        field_of_study = ""

        if education.field_of_study:
            field_of_study = f" | {escape(education.field_of_study)}"

        entries.append(f"""
            <article class="entry">
                <h3>
                    {escape(education.degree)}
                </h3>

                <div class="meta">
                    {escape(education.institution)}
                    {field_of_study}

                    <span class="dates">
                        {escape(dates)}
                    </span>
                </div>

                {
                    f"<p>{escape(education.description)}</p>"
                    if education.description
                    else ""
                }
            </article>
            """)

    return f"""
<section class="section">
    <h2>Education</h2>
    {"".join(entries)}
</section>
"""


def render_skills(
    resume: Resume,
) -> str:
    if not resume.skills:
        return ""

    skills = []

    for skill in resume.skills:
        skills.append(f"""
            <span class="skill">
                {escape(skill.name)}
            </span>
            """)

    return f"""
<section class="section">
    <h2>Skills</h2>

    <div class="skills">
        {"".join(skills)}
    </div>
</section>
"""


def render_projects(
    resume: Resume,
) -> str:
    if not resume.projects:
        return ""

    entries = []

    for project in resume.projects:
        description = ""

        if project.description:
            description = f"""
            <p class="description">
                {escape(project.description)}
            </p>
            """

        technologies = ""

        if project.technologies:
            technologies = f"""
            <p class="meta">
                <strong>Technologies:</strong>
                {escape(", ".join(project.technologies))}
            </p>
            """

        entries.append(f"""
            <article class="entry">
                <h3>{escape(project.name)}</h3>

                {description}

                {technologies}

                {
                    f'<p class="meta">'
                    f'<a href="{escape(str(project.project_url))}">'
                    f'{escape(str(project.project_url))}'
                    f'</a></p>'
                    if project.project_url
                    else ""
                }
            </article>
            """)

    return f"""
<section class="section">
    <h2>Projects</h2>
    {"".join(entries)}
</section>
"""


def render_certifications(
    resume: Resume,
) -> str:
    if not resume.certifications:
        return ""

    entries = []

    for certification in resume.certifications:
        issue_date = certification.issue_date.strftime("%b %Y")

        entries.append(f"""
            <article class="entry">
                <h3>{escape(certification.name)}</h3>

                <div class="meta">
                    {escape(certification.issuing_organization)}
                    | Issued {escape(issue_date)}
                </div>

                {
                    f"<p>Credential ID: "
                    f"{escape(certification.credential_id)}</p>"
                    if certification.credential_id
                    else ""
                }
            </article>
            """)

    return f"""
<section class="section">
    <h2>Certifications</h2>
    {"".join(entries)}
</section>
"""
