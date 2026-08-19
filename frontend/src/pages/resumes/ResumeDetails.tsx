import {
  ArrowLeft,
  Award,
  BriefcaseBusiness,
  CalendarDays,
  ExternalLink,
  FileText,
  GitBranch,
  GraduationCap,
  Pencil,
  Wrench,
} from 'lucide-react'
import { Link, useParams } from 'react-router-dom'

import { Button, buttonVariants } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'

import { useResume } from '@/features/resumes/hooks/use_resumes'
import { useExperiences } from '@/features/resumes/hooks/use_experiences'
import { useEducations } from '@/features/resumes/hooks/use_educations'
import { useSkills } from '@/features/resumes/hooks/use_skills'
import { useProjects } from '@/features/resumes/hooks/use_projects'
import { useCertifications } from '@/features/resumes/hooks/use_certifications'

import { getApiErrorMessage } from '@/utils/api_error'

function ResumeDetails() {
  const { resumeId } = useParams<{ resumeId: string }>()

  const {
    data: resume,
    isLoading: isResumeLoading,
    isError: isResumeError,
    error: resumeError,
  } = useResume(resumeId ?? '')

  const { data: experiences = [], isLoading: isExperiencesLoading } =
    useExperiences(resumeId ?? '')

  const { data: educations = [], isLoading: isEducationsLoading } =
    useEducations(resumeId ?? '')

  const { data: skills = [], isLoading: isSkillsLoading } = useSkills(
    resumeId ?? '',
  )

  const { data: projects = [], isLoading: isProjectsLoading } = useProjects(
    resumeId ?? '',
  )

  const { data: certifications = [], isLoading: isCertificationsLoading } =
    useCertifications(resumeId ?? '')

  if (!resumeId) {
    return (
      <div className="mx-auto w-full max-w-5xl">
        <Card>
          <CardHeader>
            <CardTitle>Resume not found</CardTitle>

            <CardDescription>
              The requested resume could not be identified.
            </CardDescription>
          </CardHeader>

          <CardContent>
            <Link
              to="/resumes"
              className={buttonVariants({ variant: 'outline' })}
            >
              <ArrowLeft />
              Back to resumes
            </Link>
          </CardContent>
        </Card>
      </div>
    )
  }

  if (isResumeLoading) {
    return <ResumeDetailsSkeleton />
  }

  if (isResumeError || !resume) {
    return (
      <div className="mx-auto w-full max-w-5xl">
        <Card>
          <CardHeader>
            <CardTitle>Unable to load resume</CardTitle>

            <CardDescription>{getApiErrorMessage(resumeError)}</CardDescription>
          </CardHeader>

          <CardContent className="flex flex-wrap gap-2">
            <Link
              to="/resumes"
              className={buttonVariants({ variant: 'outline' })}
            >
              <ArrowLeft />
              Back to Resumes
            </Link>

            <Button onClick={() => window.location.reload()}>Try again</Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  const isContentLoading =
    isExperiencesLoading ||
    isEducationsLoading ||
    isSkillsLoading ||
    isProjectsLoading ||
    isCertificationsLoading

  return (
    <div className="mx-auto w-full max-w-5xl space-y-8">
      <section className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div className="min-w-0">
          <Link
            to="/resumes"
            className={buttonVariants({
              variant: 'outline',
              size: 'sm',
            })}
          >
            <ArrowLeft />
            Back to resumes
          </Link>

          <div className="mt-6 flex flex-wrap items-center gap-2">
            <p className="text-sm font-medium text-primary">Resume Details</p>

            {resume.is_default && (
              <span className="rounded-full bg-primary/10 px-2 py-1 text-xs font-medium text-primary">
                Default
              </span>
            )}
          </div>

          <h1 className="mt-1 text-3xl font-semibold tracking-tight sm:text-4xl">
            {resume.title}
          </h1>

          <p className="mt-2 text-sm text-muted-foreground">
            Last updated {formatDate(resume.updated_at)}
          </p>
        </div>

        <div className="flex flex-wrap gap-2">
          <Link
            to={`/resumes/${resume.id}/edit`}
            className={buttonVariants({ variant: 'outline' })}
          >
            <Pencil />
            Edit Resume
          </Link>

          <Link
            to={`/resumes/${resume.id}/manage`}
            className={buttonVariants()}
          >
            Manage Resume
          </Link>
        </div>
      </section>

      <Card>
        <CardHeader>
          <CardTitle>Professional Summary</CardTitle>

          <CardDescription>
            The professional summary included in this resume.
          </CardDescription>
        </CardHeader>

        <CardContent>
          <p className="whitespace-pre-wrap text-sm leading-7 text-muted-foreground">
            {resume.summary || 'No professional summary has been added yet.'}
          </p>
        </CardContent>
      </Card>

      {isContentLoading && (
        <div className="rounded-lg border bg-muted/30 px-4 py-3 text-sm text-muted-foreground">
          Loading resume content...
        </div>
      )}

      <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
        <SummaryCard
          icon={BriefcaseBusiness}
          label="Experience"
          count={experiences.length}
        />

        <SummaryCard
          icon={GraduationCap}
          label="Education"
          count={educations.length}
        />

        <SummaryCard icon={Wrench} label="Skills" count={skills.length} />

        <SummaryCard icon={FileText} label="Projects" count={projects.length} />

        <SummaryCard
          icon={Award}
          label="Certifications"
          count={certifications.length}
        />
      </section>

      <section className="space-y-4">
        <SectionHeading
          icon={BriefcaseBusiness}
          title="Experience"
          count={experiences.length}
        />

        {experiences.length === 0 ? (
          <EmptySection message="No professional experience has been added yet." />
        ) : (
          <div className="space-y-4">
            {experiences.map((experience) => (
              <Card key={experience.id}>
                <CardHeader>
                  <CardTitle>{experience.job_title}</CardTitle>

                  <CardDescription>
                    {experience.company}
                    {experience.location ? ` · ${experience.location}` : ''}
                  </CardDescription>
                </CardHeader>

                <CardContent className="space-y-3">
                  <div className="flex flex-wrap items-center gap-3 text-sm text-muted-foreground">
                    <span>
                      {formatDate(experience.start_date)} -{' '}
                      {experience.is_current
                        ? 'Present'
                        : experience.end_date
                          ? formatDate(experience.end_date)
                          : 'Present'}
                    </span>

                    <span>
                      {formatEmploymentType(experience.employment_type)}
                    </span>
                  </div>

                  {experience.description && (
                    <p className="whitespace-pre-wrap text-sm leading-6 text-muted-foreground">
                      {experience.description}
                    </p>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </section>

      <section className="space-y-4">
        <SectionHeading
          icon={GraduationCap}
          title="Education"
          count={educations.length}
        />

        {educations.length === 0 ? (
          <EmptySection message="No education information has been added yet." />
        ) : (
          <div className="space-y-4">
            {educations.map((education) => (
              <Card key={education.id}>
                <CardHeader>
                  <CardTitle>{education.degree}</CardTitle>

                  <CardDescription>
                    {education.institution}
                    {education.field_of_study
                      ? ` · ${education.field_of_study}`
                      : ''}
                  </CardDescription>
                </CardHeader>

                <CardContent className="space-y-3">
                  <div className="flex flex-wrap items-center gap-3 text-sm text-muted-foreground">
                    <span>
                      {formatDate(education.start_date)} -{' '}
                      {education.is_current
                        ? 'Present'
                        : education.end_date
                          ? formatDate(education.end_date)
                          : 'Present'}
                    </span>

                    {education.location && <span>{education.location}</span>}

                    {education.grade && <span>Grade: {education.grade}</span>}
                  </div>

                  {education.description && (
                    <p className="whitespace-pre-wrap text-sm leading-6 text-muted-foreground">
                      {education.description}
                    </p>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </section>

      <section className="space-y-4">
        <SectionHeading icon={Wrench} title="Skills" count={skills.length} />

        {skills.length === 0 ? (
          <EmptySection message="No skills have been added yet." />
        ) : (
          <Card>
            <CardContent className="flex flex-wrap gap-2 pt-6">
              {skills.map((skill) => (
                <div
                  key={skill.id}
                  className="rounded-full border bg-muted/30 px-3 py-1.5 text-sm"
                >
                  <span className="font-medium">{skill.name}</span>

                  <span className="ml-2 text-muted-foreground">
                    {formatSkillLevel(skill.proficiency)}
                  </span>
                </div>
              ))}
            </CardContent>
          </Card>
        )}
      </section>

      <section className="space-y-4">
        <SectionHeading
          icon={FileText}
          title="Projects"
          count={projects.length}
        />

        {projects.length === 0 ? (
          <EmptySection message="No projects have been added yet." />
        ) : (
          <div className="space-y-4">
            {projects.map((project) => (
              <Card key={project.id}>
                <CardHeader>
                  <CardTitle>{project.name}</CardTitle>

                  <CardDescription>{project.technologies}</CardDescription>
                </CardHeader>

                <CardContent className="space-y-4">
                  <p className="whitespace-pre-wrap text-sm leading-6 text-muted-foreground">
                    {project.description}
                  </p>

                  <div className="flex flex-wrap gap-2">
                    {project.project_url && (
                      <a
                        href={project.project_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className={buttonVariants({
                          variant: 'outline',
                          size: 'sm',
                        })}
                      >
                        <ExternalLink />
                        Live Project
                      </a>
                    )}

                    {project.repository_url && (
                      <a
                        href={project.repository_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className={buttonVariants({
                          variant: 'outline',
                          size: 'sm',
                        })}
                      >
                        <GitBranch />
                        Repository
                      </a>
                    )}
                  </div>

                  {(project.start_date || project.end_date) && (
                    <div className="flex items-center gap-2 text-sm text-muted-foreground">
                      <CalendarDays className="size-4" />

                      <span>
                        {project.start_date
                          ? formatDate(project.start_date)
                          : 'No start date'}{' '}
                        -{' '}
                        {project.is_ongoing
                          ? 'Present'
                          : project.end_date
                            ? formatDate(project.end_date)
                            : 'No end date'}
                      </span>
                    </div>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </section>

      <section className="space-y-4">
        <SectionHeading
          icon={Award}
          title="Certifications"
          count={certifications.length}
        />

        {certifications.length === 0 ? (
          <EmptySection message="No certifications have been added yet." />
        ) : (
          <div className="space-y-4">
            {certifications.map((certification) => (
              <Card key={certification.id}>
                <CardHeader>
                  <CardTitle>{certification.name}</CardTitle>

                  <CardDescription>
                    {certification.issuing_organization}
                  </CardDescription>
                </CardHeader>

                <CardContent className="space-y-3">
                  <div className="flex flex-wrap items-center gap-3 text-sm text-muted-foreground">
                    <span>Issued {formatDate(certification.issue_date)}</span>

                    {certification.does_not_expire ? (
                      <span>Does not expire</span>
                    ) : (
                      certification.expiration_date && (
                        <span>
                          Expires {formatDate(certification.expiration_date)}
                        </span>
                      )
                    )}
                  </div>

                  {certification.credential_id && (
                    <p className="text-sm text-muted-foreground">
                      <span className="font-medium text-foreground">
                        Credential ID:
                      </span>{' '}
                      {certification.credential_id}
                    </p>
                  )}

                  {certification.credential_url && (
                    <a
                      href={certification.credential_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className={buttonVariants({
                        variant: 'outline',
                        size: 'sm',
                      })}
                    >
                      <ExternalLink />
                      Verify Credential
                    </a>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </section>

      {resume.generated_content && (
        <Card>
          <CardHeader>
            <CardTitle>Generated Content</CardTitle>

            <CardDescription>
              AI-generated content associated with this resume.
            </CardDescription>
          </CardHeader>

          <CardContent>
            <p className="whitespace-pre-wrap text-sm leading-7 text-muted-foreground">
              {resume.generated_content}
            </p>

            {resume.generated_at && (
              <p className="mt-4 text-xs text-muted-foreground">
                Generated {formatDate(resume.generated_at)}
              </p>
            )}
          </CardContent>
        </Card>
      )}

      <Card>
        <CardHeader>
          <CardTitle>Resume Information</CardTitle>

          <CardDescription>Metadata for this resume.</CardDescription>
        </CardHeader>

        <CardContent className="grid gap-4 sm:grid-cols-3">
          <MetadataItem
            label="Default Resume"
            value={resume.is_default ? 'Yes' : 'No'}
          />

          <MetadataItem label="Created" value={formatDate(resume.created_at)} />

          <MetadataItem
            label="Last Updated"
            value={formatDate(resume.updated_at)}
          />
        </CardContent>
      </Card>
    </div>
  )
}

function ResumeDetailsSkeleton() {
  return (
    <div className="mx-auto w-full max-w-5xl space-y-8">
      <div className="space-y-3">
        <div className="h-9 w-32 animate-pulse rounded bg-muted" />
        <div className="h-10 w-2/3 animate-pulse rounded bg-muted" />
        <div className="h-4 w-48 animate-pulse rounded bg-muted" />
      </div>

      <Card>
        <CardHeader>
          <div className="h-6 w-48 animate-pulse rounded bg-muted" />
          <div className="h-4 w-72 animate-pulse rounded bg-muted" />
        </CardHeader>

        <CardContent>
          <div className="h-20 w-full animate-pulse rounded bg-muted" />
        </CardContent>
      </Card>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
        {Array.from({ length: 5 }).map((_, index) => (
          <Card key={index}>
            <CardContent className="space-y-3 pt-6">
              <div className="h-5 w-5 animate-pulse rounded bg-muted" />
              <div className="h-4 w-24 animate-pulse rounded bg-muted" />
              <div className="h-7 w-12 animate-pulse rounded bg-muted" />
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}

interface SummaryCardProps {
  icon: typeof BriefcaseBusiness
  label: string
  count: number
}

function SummaryCard({ icon: Icon, label, count }: SummaryCardProps) {
  return (
    <Card>
      <CardContent className="pt-6">
        <Icon className="size-5 text-primary" />

        <p className="mt-3 text-sm text-muted-foreground">{label}</p>

        <p className="mt-1 text-2xl font-semibold">{count}</p>
      </CardContent>
    </Card>
  )
}

interface SectionHeadingProps {
  icon: typeof BriefcaseBusiness
  title: string
  count: number
}

function SectionHeading({ icon: Icon, title, count }: SectionHeadingProps) {
  return (
    <div className="flex items-center gap-3">
      <Icon className="size-5 text-primary" />

      <h2 className="text-xl font-semibold tracking-tight">{title}</h2>

      <span className="rounded-full bg-muted px-2 py-0.5 text-xs font-medium text-muted-foreground">
        {count}
      </span>
    </div>
  )
}

function EmptySection({ message }: { message: string }) {
  return (
    <Card>
      <CardContent className="pt-6">
        <p className="text-sm text-muted-foreground">{message}</p>
      </CardContent>
    </Card>
  )
}

function MetadataItem({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg border p-4">
      <p className="text-sm text-muted-foreground">{label}</p>

      <p className="mt-1 font-medium">{value}</p>
    </div>
  )
}

function formatDate(value: string) {
  return new Date(value).toLocaleDateString()
}

function formatEmploymentType(value: string) {
  return value
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (character) => character.toUpperCase())
}

function formatSkillLevel(value: string) {
  return value
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (character) => character.toUpperCase())
}

export default ResumeDetails
