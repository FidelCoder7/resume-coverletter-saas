import {
  BriefcaseBusiness,
  ChevronLeft,
  Pencil,
  Plus,
  Trash2,
} from 'lucide-react'
import { useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'

import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import ExperienceForm from '@/features/resumes/components/ExperienceForm'
import {
  useCreateExperience,
  useDeleteExperience,
  useExperiences,
  useUpdateExperience,
} from '@/features/resumes/hooks/use_experiences'
import { useResume } from '@/features/resumes/hooks/use_resumes'
import type { Experience } from '@/features/resumes/types'
import type { ExperienceFormValues } from '@/features/resumes/schemas/experience_schemas'
import { buttonVariants } from '@/components/ui/button'
import { getApiErrorMessage } from '@/utils/api_error'

function ExperienceManagement() {
  const { resumeId } = useParams<{ resumeId: string }>()
  const navigate = useNavigate()

  const [isCreating, setIsCreating] = useState(false)
  const [editingExperience, setEditingExperience] = useState<Experience | null>(
    null,
  )

  const {
    data: resume,
    isLoading: isResumeLoading,
    isError: isResumeError,
    error: resumeError,
  } = useResume(resumeId ?? '')

  const {
    data: experiences = [],
    isLoading: isExperiencesLoading,
    isError: isExperiencesError,
    error: experiencesError,
  } = useExperiences(resumeId ?? '')

  const createMutation = useCreateExperience()
  const updateMutation = useUpdateExperience()
  const deleteMutation = useDeleteExperience()

  const isSubmitting = createMutation.isPending || updateMutation.isPending

  function buildExperiencePayload(values: ExperienceFormValues) {
    return {
      ...values,
      location: values.location || null,
      description: values.description || null,
      end_date: values.is_current ? null : values.end_date || null,
    }
  }

  function handleCreate(values: ExperienceFormValues) {
    if (!resumeId) {
      return
    }

    createMutation.mutate(
      {
        resumeId,
        payload: buildExperiencePayload(values),
      },
      {
        onSuccess: () => {
          setIsCreating(false)
        },
      },
    )
  }

  function handleUpdate(values: ExperienceFormValues) {
    if (!editingExperience) {
      return
    }

    updateMutation.mutate(
      {
        experienceId: editingExperience.id,
        payload: buildExperiencePayload(values),
      },
      {
        onSuccess: () => {
          setEditingExperience(null)
        },
      },
    )
  }

  function handleDelete(experience: Experience) {
    if (!resumeId) {
      return
    }

    const confirmed = window.confirm(
      `Are you sure you want to delete your ${experience.job_title} position at ${experience.company}? This action cannot be undone.`,
    )

    if (!confirmed) {
      return
    }

    deleteMutation.mutate({
      experienceId: experience.id,
      resumeId,
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
            <Button onClick={() => navigate('/resumes')}>
              Back to resumes
            </Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  if (isResumeLoading || isExperiencesLoading) {
    return (
      <div className="mx-auto w-full max-w-7xl space-y-6">
        <div className="h-10 w-40 animate-pulse rounded bg-muted" />

        <div>
          <div className="h-8 w-1/3 animate-pulse rounded bg-muted" />

          <div className="mt-2 h-5 w-2/3 animate-pulse rounded bg-muted" />
        </div>

        <Card>
          <CardHeader>
            <div className="h-6 w-1/3 animate-pulse rounded bg-muted" />

            <div className="h-4 w-2/3 animate-pulse rounded bg-muted" />
          </CardHeader>

          <CardContent className="space-y-4">
            {[1, 2].map((item) => (
              <div
                key={item}
                className="h-32 animate-pulse rounded-lg bg-muted"
              />
            ))}
          </CardContent>
        </Card>
      </div>
    )
  }

  if (isResumeError || !resume) {
    return (
      <div className="mx-auto w-full max-w-7xl">
        <Card>
          <CardHeader>
            <CardTitle>Unable to load resume</CardTitle>

            <CardDescription>{getApiErrorMessage(resumeError)}</CardDescription>
          </CardHeader>

          <CardContent className="flex gap-2">
            <Button variant="outline" onClick={() => navigate('/resumes')}>
              Back to resumes
            </Button>

            <Button onClick={() => window.location.reload()}>Try again</Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  if (isExperiencesError) {
    return (
      <div className="mx-auto w-full max-w-7xl space-y-6">
        <Link
          to={`/resumes/${resumeId}`}
          className={buttonVariants({
            variant: 'outline',
          })}
        >
          <ChevronLeft />
          Back to resume
        </Link>

        <Card>
          <CardHeader>
            <CardTitle>Unable to load experience</CardTitle>

            <CardDescription>
              {getApiErrorMessage(experiencesError)}
            </CardDescription>
          </CardHeader>

          <CardContent>
            <Button onClick={() => window.location.reload()}>Try again</Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="mx-auto w-full max-w-7xl space-y-8">
      <div>
        <Link
          to={`/resumes/${resumeId}`}
          className={buttonVariants({
            variant: 'outline',
          })}
        >
          <ChevronLeft />
          Back to resume
        </Link>
      </div>

      <section className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="text-sm font-medium text-primary">Resume Editor</p>

          <h2 className="mt-1 text-2xl font-semibold tracking-tight sm:text-3xl">
            Experience
          </h2>

          <p className="mt-2 text-muted-foreground">
            Manage your professional experience for{' '}
            <span className="font-medium text-foreground">{resume.title}</span>.
          </p>
        </div>

        {!isCreating && !editingExperience && (
          <Button onClick={() => setIsCreating(true)}>
            <Plus />
            Add Experience
          </Button>
        )}
      </section>

      {createMutation.isError && (
        <Card>
          <CardContent className="pt-6">
            <p className="text-sm text-destructive">
              {getApiErrorMessage(createMutation.error)}
            </p>
          </CardContent>
        </Card>
      )}

      {updateMutation.isError && (
        <Card>
          <CardContent className="pt-6">
            <p className="text-sm text-destructive">
              {getApiErrorMessage(updateMutation.error)}
            </p>
          </CardContent>
        </Card>
      )}

      {isCreating && (
        <ExperienceForm
          isSubmitting={isSubmitting}
          onSubmit={handleCreate}
          onCancel={() => setIsCreating(false)}
        />
      )}

      {editingExperience && (
        <ExperienceForm
          experience={editingExperience}
          isSubmitting={isSubmitting}
          onSubmit={handleUpdate}
          onCancel={() => setEditingExperience(null)}
        />
      )}

      {!isCreating && !editingExperience && (
        <Card>
          <CardHeader>
            <div className="flex items-center gap-3">
              <BriefcaseBusiness className="size-6 text-primary" />

              <div>
                <CardTitle>Professional Experience</CardTitle>

                <CardDescription>
                  Add your work history, responsibilities, and achievements.
                </CardDescription>
              </div>
            </div>
          </CardHeader>

          <CardContent>
            {experiences.length === 0 ? (
              <div className="flex flex-col items-center justify-center rounded-lg border border-dashed p-10 text-center">
                <BriefcaseBusiness className="size-10 text-muted-foreground" />

                <h3 className="mt-4 font-semibold">No experience added yet</h3>

                <p className="mt-2 max-w-md text-sm text-muted-foreground">
                  Add your professional experience to help employers understand
                  your career history and achievements.
                </p>

                <Button className="mt-6" onClick={() => setIsCreating(true)}>
                  <Plus />
                  Add your first experience
                </Button>
              </div>
            ) : (
              <div className="space-y-4">
                {experiences.map((experience) => (
                  <ExperienceCard
                    key={experience.id}
                    experience={experience}
                    isDeleting={
                      deleteMutation.isPending &&
                      deleteMutation.variables?.experienceId === experience.id
                    }
                    onEdit={() => setEditingExperience(experience)}
                    onDelete={() => handleDelete(experience)}
                  />
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  )
}

interface ExperienceCardProps {
  experience: Experience
  isDeleting: boolean
  onEdit: () => void
  onDelete: () => void
}

function ExperienceCard({
  experience,
  isDeleting,
  onEdit,
  onDelete,
}: ExperienceCardProps) {
  return (
    <div className="rounded-lg border p-5">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div className="min-w-0">
          <h3 className="text-lg font-semibold">{experience.job_title}</h3>

          <p className="mt-1 font-medium text-primary">{experience.company}</p>

          <div className="mt-2 flex flex-wrap gap-x-3 gap-y-1 text-sm text-muted-foreground">
            {experience.location && <span>{experience.location}</span>}

            <span>{formatEmploymentType(experience.employment_type)}</span>
          </div>

          <p className="mt-2 text-sm text-muted-foreground">
            {formatDate(experience.start_date)} -{' '}
            {experience.is_current
              ? 'Present'
              : experience.end_date
                ? formatDate(experience.end_date)
                : 'N/A'}
          </p>
        </div>

        <div className="flex shrink-0 gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={onEdit}
            disabled={isDeleting}
          >
            <Pencil />
            Edit
          </Button>

          <Button
            variant="destructive"
            size="sm"
            onClick={onDelete}
            disabled={isDeleting}
          >
            <Trash2 />

            {isDeleting ? 'Deleting...' : 'Delete'}
          </Button>
        </div>
      </div>

      {experience.description && (
        <p className="mt-4 whitespace-pre-wrap text-sm leading-6 text-muted-foreground">
          {experience.description}
        </p>
      )}
    </div>
  )
}

function formatDate(value: string) {
  return new Date(`${value}T00:00:00`).toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'short',
  })
}

function formatEmploymentType(value: string) {
  return value
    .split('_')
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

export default ExperienceManagement
