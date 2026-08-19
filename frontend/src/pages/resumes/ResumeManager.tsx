import {
  Award,
  BriefcaseBusiness,
  ChevronLeft,
  FileText,
  GraduationCap,
  Pencil,
  ScrollText,
  Sparkles,
  Trash2,
  Wrench,
} from 'lucide-react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import type { ComponentType } from 'react'

import { Button, buttonVariants } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'

import {
  useDeleteResume,
  useResume,
} from '@/features/resumes/hooks/use_resumes'
import { useExperiences } from '@/features/resumes/hooks/use_experiences'
import { useEducations } from '@/features/resumes/hooks/use_educations'
import { useSkills } from '@/features/resumes/hooks/use_skills'
import { useProjects } from '@/features/resumes/hooks/use_projects'
import { useCertifications } from '@/features/resumes/hooks/use_certifications'

import { getApiErrorMessage } from '@/utils/api_error'

function ResumeManager() {
  const { resumeId } = useParams<{ resumeId: string }>()
  const navigate = useNavigate()

  const { data: resume, isLoading, isError, error } = useResume(resumeId ?? '')

  const experiencesQuery = useExperiences(resumeId ?? '')
  const educationsQuery = useEducations(resumeId ?? '')
  const skillsQuery = useSkills(resumeId ?? '')
  const projectsQuery = useProjects(resumeId ?? '')
  const certificationsQuery = useCertifications(resumeId ?? '')

  const deleteMutation = useDeleteResume()

  function handleDelete() {
    if (!resumeId || !resume) {
      return
    }

    const confirmed = window.confirm(
      `Are you sure you want to delete "${resume.title}"? This action cannot be undone.`,
    )

    if (!confirmed) {
      return
    }

    deleteMutation.mutate(resumeId, {
      onSuccess: () => {
        navigate('/resumes')
      },
    })
  }

  if (!resumeId) {
    return (
      <div className="mx-auto w-full max-w-7xl">
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
              Back to resumes
            </Link>
          </CardContent>
        </Card>
      </div>
    )
  }

  if (isLoading) {
    return (
      <div className="mx-auto w-full max-w-7xl space-y-6">
        <div className="h-5 w-24 animate-pulse rounded bg-muted" />

        <Card>
          <CardHeader>
            <div className="h-7 w-1/2 animate-pulse rounded bg-muted" />

            <div className="h-4 w-3/4 animate-pulse rounded bg-muted" />
          </CardHeader>

          <CardContent className="space-y-4">
            <div className="h-20 w-full animate-pulse rounded bg-muted" />

            <div className="h-9 w-28 animate-pulse rounded bg-muted" />
          </CardContent>
        </Card>
      </div>
    )
  }

  if (isError || !resume) {
    return (
      <div className="mx-auto w-full max-w-7xl">
        <Card>
          <CardHeader>
            <CardTitle>Unable to load resume</CardTitle>

            <CardDescription>{getApiErrorMessage(error)}</CardDescription>
          </CardHeader>

          <CardContent className="flex gap-2">
            <Button variant="outline" onClick={() => navigate('/resumes')}>
              Back to Resumes
            </Button>

            <Button onClick={() => window.location.reload()}>Try again</Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  const experienceCount = experiencesQuery.data?.length ?? 0
  const educationCount = educationsQuery.data?.length ?? 0
  const skillCount = skillsQuery.data?.length ?? 0
  const projectCount = projectsQuery.data?.length ?? 0
  const certificationCount = certificationsQuery.data?.length ?? 0

  const contentCount =
    experienceCount +
    educationCount +
    skillCount +
    projectCount +
    certificationCount

  const isLoadingDetails =
    experiencesQuery.isLoading ||
    educationsQuery.isLoading ||
    skillsQuery.isLoading ||
    projectsQuery.isLoading ||
    certificationsQuery.isLoading

  return (
    <div className="mx-auto w-full max-w-7xl space-y-8">
      <div>
        <Link to="/resumes" className={buttonVariants({ variant: 'outline' })}>
          <ChevronLeft />
          Back to resumes
        </Link>
      </div>

      <section className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div className="min-w-0">
          <div className="flex flex-wrap items-center gap-2">
            <p className="text-sm font-medium text-primary">Resume Manager</p>

            {resume.is_default && (
              <span className="rounded-full bg-primary/10 px-2 py-1 text-xs font-medium text-primary">
                Default
              </span>
            )}
          </div>

          <h2 className="mt-1 truncate text-2xl font-semibold tracking-tight sm:text-3xl">
            {resume.title}
          </h2>

          <p className="mt-2 text-sm text-muted-foreground">
            Last updated {new Date(resume.updated_at).toLocaleDateString()}
          </p>
        </div>

        <div className="flex flex-wrap gap-2">
          <Link
            to={`/resumes/${resume.id}/edit`}
            className={buttonVariants({ variant: 'outline' })}
          >
            <Pencil />
            Edit Details
          </Link>

          <Button
            variant="destructive"
            disabled={deleteMutation.isPending}
            onClick={handleDelete}
          >
            <Trash2 />
            {deleteMutation.isPending ? 'Deleting...' : 'Delete'}
          </Button>
        </div>
      </section>

      {deleteMutation.isError && (
        <Card>
          <CardContent className="pt-6">
            <p className="text-sm text-destructive">
              {getApiErrorMessage(deleteMutation.error)}
            </p>
          </CardContent>
        </Card>
      )}

      <Card>
        <CardHeader>
          <div className="flex items-center gap-3">
            <FileText className="size-6 text-primary" />

            <div>
              <CardTitle>Resume Overview</CardTitle>

              <CardDescription>
                Review the core information and content that make up this
                resume.
              </CardDescription>
            </div>
          </div>
        </CardHeader>

        <CardContent className="space-y-6">
          <div>
            <p className="whitespace-pre-wrap text-sm leading-6 text-muted-foreground">
              {resume.summary || 'No professional summary has been added yet.'}
            </p>
          </div>

          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <StatusItem
              label="Resume Sections"
              value={isLoadingDetails ? 'Loading...' : `${contentCount} items`}
            />

            <StatusItem
              label="Default Resume"
              value={resume.is_default ? 'Yes' : 'No'}
            />

            <StatusItem
              label="AI Generated Content"
              value={resume.generated_content ? 'Available' : 'Not generated'}
            />
          </div>
        </CardContent>
      </Card>

      <section>
        <div className="mb-4">
          <h3 className="text-lg font-semibold">Resume Content</h3>

          <p className="mt-1 text-sm text-muted-foreground">
            Manage the sections that make up your professional resume.
          </p>
        </div>

        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <ResumeSectionCard
            icon={BriefcaseBusiness}
            title="Experience"
            description="Add and manage your professional work experience."
            count={experienceCount}
            isLoading={experiencesQuery.isLoading}
            to={`/resumes/${resume.id}/experience`}
          />

          <ResumeSectionCard
            icon={GraduationCap}
            title="Education"
            description="Manage your academic background and qualifications."
            count={educationCount}
            isLoading={educationsQuery.isLoading}
            to={`/resumes/${resume.id}/education`}
          />

          <ResumeSectionCard
            icon={Wrench}
            title="Skills"
            description="Add technical and professional skills to your resume."
            count={skillCount}
            isLoading={skillsQuery.isLoading}
            to={`/resumes/${resume.id}/skills`}
          />

          <ResumeSectionCard
            icon={ScrollText}
            title="Projects"
            description="Showcase projects and the technologies you've used."
            count={projectCount}
            isLoading={projectsQuery.isLoading}
            to={`/resumes/${resume.id}/projects`}
          />

          <ResumeSectionCard
            icon={Award}
            title="Certifications"
            description="Manage professional certifications and credentials."
            count={certificationCount}
            isLoading={certificationsQuery.isLoading}
            to={`/resumes/${resume.id}/certifications`}
          />

          <ResumeSectionCard
            icon={Sparkles}
            title="AI Resume Tools"
            description="Generate, improve, and optimize this resume with AI."
          />
        </div>
      </section>

      <Card>
        <CardHeader>
          <CardTitle>Resume Status</CardTitle>

          <CardDescription>
            Information about this resume and its generated content.
          </CardDescription>
        </CardHeader>

        <CardContent className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <StatusItem
            label="Default Resume"
            value={resume.is_default ? 'Yes' : 'No'}
          />

          <StatusItem
            label="AI Generated Content"
            value={resume.generated_content ? 'Available' : 'Not generated'}
          />

          <StatusItem
            label="Last Updated"
            value={new Date(resume.updated_at).toLocaleDateString()}
          />
        </CardContent>
      </Card>
    </div>
  )
}

interface ResumeSectionCardProps {
  icon: ComponentType<{ className?: string }>
  title: string
  description: string
  count?: number
  isLoading?: boolean
  to?: string
}

function ResumeSectionCard({
  icon: Icon,
  title,
  description,
  count,
  isLoading = false,
  to,
}: ResumeSectionCardProps) {
  return (
    <Card className="transition-shadow hover:shadow-md">
      <CardHeader>
        <Icon className="mb-2 size-6 text-primary" />

        <div className="flex items-center justify-between gap-3">
          <CardTitle>{title}</CardTitle>

          {count !== undefined && (
            <span className="rounded-full bg-muted px-2.5 py-1 text-xs font-medium">
              {isLoading ? '...' : count}
            </span>
          )}
        </div>

        <CardDescription>{description}</CardDescription>
      </CardHeader>

      <CardContent>
        {to ? (
          <Link to={to} className={buttonVariants({ variant: 'outline' })}>
            Manage
          </Link>
        ) : (
          <Button variant="outline" disabled>
            Coming soon
          </Button>
        )}
      </CardContent>
    </Card>
  )
}

interface StatusItemProps {
  label: string
  value: string
}

function StatusItem({ label, value }: StatusItemProps) {
  return (
    <div className="rounded-lg border p-4">
      <p className="text-sm text-muted-foreground">{label}</p>

      <p className="mt-1 font-medium">{value}</p>
    </div>
  )
}

export default ResumeManager
