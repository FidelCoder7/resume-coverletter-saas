import { ChevronLeft, GraduationCap, Pencil, Plus, Trash2 } from 'lucide-react'
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
import EducationForm from '@/features/resumes/components/EducationForm'
import {
  useCreateEducation,
  useDeleteEducation,
  useEducations,
  useUpdateEducation,
} from '@/features/resumes/hooks/use_educations'
import { useResume } from '@/features/resumes/hooks/use_resumes'
import type { Education } from '@/features/resumes/types'
import type { EducationFormValues } from '@/features/resumes/schemas/education_schemas'
import { buttonVariants } from '@/components/ui/button'
import { getApiErrorMessage } from '@/utils/api_error'

function EducationManagement() {
  const { resumeId } = useParams<{ resumeId: string }>()
  const navigate = useNavigate()

  const [isCreating, setIsCreating] = useState(false)
  const [editingEducation, setEditingEducation] = useState<Education | null>(
    null,
  )

  const {
    data: resume,
    isLoading: isResumeLoading,
    isError: isResumeError,
    error: resumeError,
  } = useResume(resumeId ?? '')

  const {
    data: educations = [],
    isLoading: isEducationsLoading,
    isError: isEducationsError,
    error: educationsError,
  } = useEducations(resumeId ?? '')

  const createMutation = useCreateEducation()
  const updateMutation = useUpdateEducation()
  const deleteMutation = useDeleteEducation()

  const isSubmitting = createMutation.isPending || updateMutation.isPending

  function handleCreate(values: EducationFormValues) {
    if (!resumeId) {
      return
    }

    createMutation.mutate(
      {
        resumeId,
        payload: {
          ...values,
          location: values.location || null,
          grade: values.grade || null,
          end_date: values.is_current ? null : values.end_date || null,
          description: values.description || null,
        },
      },
      {
        onSuccess: () => {
          setIsCreating(false)
        },
      },
    )
  }

  function handleUpdate(values: EducationFormValues) {
    if (!editingEducation) {
      return
    }

    updateMutation.mutate(
      {
        educationId: editingEducation.id,
        payload: {
          ...values,
          location: values.location || null,
          grade: values.grade || null,
          end_date: values.is_current ? null : values.end_date || null,
          description: values.description || null,
        },
      },
      {
        onSuccess: () => {
          setEditingEducation(null)
        },
      },
    )
  }

  function handleDelete(education: Education) {
    if (!resumeId) {
      return
    }

    const confirmed = window.confirm(
      `Are you sure you want to delete your ${education.degree} at ${education.institution}? This action cannot be undone.`,
    )

    if (!confirmed) {
      return
    }

    deleteMutation.mutate({
      educationId: education.id,
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

  if (isResumeLoading || isEducationsLoading) {
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

  if (isEducationsError) {
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
            <CardTitle>Unable to load education</CardTitle>

            <CardDescription>
              {getApiErrorMessage(educationsError)}
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
            Education
          </h2>

          <p className="mt-2 text-muted-foreground">
            Manage your academic background for{' '}
            <span className="font-medium text-foreground">{resume.title}</span>.
          </p>
        </div>

        {!isCreating && !editingEducation && (
          <Button onClick={() => setIsCreating(true)}>
            <Plus />
            Add Education
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

      {deleteMutation.isError && (
        <Card>
          <CardContent className="pt-6">
            <p className="text-sm text-destructive">
              {getApiErrorMessage(deleteMutation.error)}
            </p>
          </CardContent>
        </Card>
      )}

      {isCreating && (
        <EducationForm
          isSubmitting={isSubmitting}
          onSubmit={handleCreate}
          onCancel={() => setIsCreating(false)}
        />
      )}

      {editingEducation && (
        <EducationForm
          education={editingEducation}
          isSubmitting={isSubmitting}
          onSubmit={handleUpdate}
          onCancel={() => setEditingEducation(null)}
        />
      )}

      {!isCreating && !editingEducation && (
        <Card>
          <CardHeader>
            <div className="flex items-center gap-3">
              <GraduationCap className="size-6 text-primary" />

              <div>
                <CardTitle>Academic Education</CardTitle>

                <CardDescription>
                  Add your academic background, qualifications, and
                  achievements.
                </CardDescription>
              </div>
            </div>
          </CardHeader>

          <CardContent>
            {educations.length === 0 ? (
              <div className="flex flex-col items-center justify-center rounded-lg border border-dashed p-10 text-center">
                <GraduationCap className="size-10 text-muted-foreground" />

                <h3 className="mt-4 font-semibold">No education added yet</h3>

                <p className="mt-2 max-w-md text-sm text-muted-foreground">
                  Add your academic background to help employers understand your
                  qualifications and educational achievements.
                </p>

                <Button className="mt-6" onClick={() => setIsCreating(true)}>
                  <Plus />
                  Add your first education
                </Button>
              </div>
            ) : (
              <div className="space-y-4">
                {educations.map((education) => (
                  <EducationCard
                    key={education.id}
                    education={education}
                    isDeleting={
                      deleteMutation.isPending &&
                      deleteMutation.variables?.educationId === education.id
                    }
                    onEdit={() => setEditingEducation(education)}
                    onDelete={() => handleDelete(education)}
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

interface EducationCardProps {
  education: Education
  isDeleting: boolean
  onEdit: () => void
  onDelete: () => void
}

function EducationCard({
  education,
  isDeleting,
  onEdit,
  onDelete,
}: EducationCardProps) {
  return (
    <div className="rounded-lg border p-5">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div className="min-w-0">
          <h3 className="text-lg font-semibold">{education.degree}</h3>

          <p className="mt-1 font-medium text-primary">
            {education.institution}
          </p>

          <p className="mt-1 text-sm text-muted-foreground">
            {education.field_of_study}
          </p>

          <div className="mt-2 flex flex-wrap gap-x-3 gap-y-1 text-sm text-muted-foreground">
            {education.location && <span>{education.location}</span>}

            {education.grade && <span>Grade: {education.grade}</span>}
          </div>

          <p className="mt-2 text-sm text-muted-foreground">
            {formatDate(education.start_date)} -{' '}
            {education.is_current
              ? 'Present'
              : education.end_date
                ? formatDate(education.end_date)
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

      {education.description && (
        <p className="mt-4 whitespace-pre-wrap text-sm leading-6 text-muted-foreground">
          {education.description}
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

export default EducationManagement
