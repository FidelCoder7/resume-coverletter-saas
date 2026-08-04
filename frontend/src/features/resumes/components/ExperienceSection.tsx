import { Briefcase, Pencil, Plus, Trash2 } from 'lucide-react'
import { useState } from 'react'

import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

import {
  useCreateExperience,
  useDeleteExperience,
  useExperiences,
  useUpdateExperience,
} from '@/features/resumes/hooks/use_experiences'

import type { Experience } from '@/features/resumes/types'

import { getApiErrorMessage } from '@/utils/api_error'

import ExperienceForm from './ExperienceForm'

import type { ExperienceFormValues } from '@/features/resumes/schemas/experience_schemas'

interface ExperienceSectionProps {
  resumeId: string
}

function ExperienceSection({ resumeId }: ExperienceSectionProps) {
  const [isCreating, setIsCreating] = useState(false)

  const [editingExperience, setEditingExperience] = useState<Experience | null>(
    null,
  )

  const experiencesQuery = useExperiences(resumeId)

  const createMutation = useCreateExperience()

  const updateMutation = useUpdateExperience()

  const deleteMutation = useDeleteExperience()

  function handleCreate(values: ExperienceFormValues) {
    createMutation.mutate(
      {
        resumeId,
        payload: {
          ...values,
          location: values.location || null,
          end_date: values.end_date || null,
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

  function handleUpdate(values: ExperienceFormValues) {
    if (!editingExperience) {
      return
    }

    updateMutation.mutate(
      {
        experienceId: editingExperience.id,
        payload: {
          ...values,
          location: values.location || null,
          end_date: values.end_date || null,
          description: values.description || null,
        },
      },
      {
        onSuccess: () => {
          setEditingExperience(null)
        },
      },
    )
  }

  function handleDelete(experience: Experience) {
    const confirmed = window.confirm(
      `Are you sure you want to delete your experience at "${experience.company}"? This action cannot be undone.`,
    )

    if (!confirmed) {
      return
    }

    deleteMutation.mutate({
      experienceId: experience.id,
      resumeId,
    })
  }

  if (isCreating || editingExperience) {
    return (
      <ExperienceForm
        experience={editingExperience ?? undefined}
        isSubmitting={createMutation.isPending || updateMutation.isPending}
        onSubmit={editingExperience ? handleUpdate : handleCreate}
        onCancel={() => {
          setIsCreating(false)
          setEditingExperience(null)
        }}
      />
    )
  }

  if (experiencesQuery.isLoading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Experience</CardTitle>
        </CardHeader>

        <CardContent>
          <div className="space-y-4">
            {[1, 2].map((item) => (
              <div key={item} className="space-y-2">
                <div className="h-5 w-1/3 animate-pulse rounded bg-muted" />

                <div className="h-4 w-1/2 animate-pulse rounded bg-muted" />

                <div className="h-16 w-full animate-pulse rounded bg-muted" />
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    )
  }

  if (experiencesQuery.isError) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Experience</CardTitle>
        </CardHeader>

        <CardContent className="space-y-4">
          <p className="text-sm text-destructive">
            {getApiErrorMessage(experiencesQuery.error)}
          </p>

          <Button variant="outline" onClick={() => experiencesQuery.refetch()}>
            Try again
          </Button>
        </CardContent>
      </Card>
    )
  }

  const experiences = experiencesQuery.data ?? []

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between gap-4">
          <div>
            <CardTitle>Experience</CardTitle>

            <p className="mt-1 text-sm text-muted-foreground">
              Add your professional work experience and career history.
            </p>
          </div>

          <Button size="sm" onClick={() => setIsCreating(true)}>
            <Plus />
            Add Experience
          </Button>
        </div>
      </CardHeader>

      <CardContent>
        {experiences.length === 0 ? (
          <div className="flex flex-col items-center justify-center gap-3 rounded-lg border border-dashed p-8 text-center">
            <Briefcase className="size-10 text-muted-foreground" />

            <div>
              <h3 className="font-medium">No experience added</h3>

              <p className="mt-1 text-sm text-muted-foreground">
                Add your work history to strengthen your resume.
              </p>
            </div>

            <Button variant="outline" onClick={() => setIsCreating(true)}>
              <Plus />
              Add your first experience
            </Button>
          </div>
        ) : (
          <div className="space-y-6">
            {experiences.map((experience) => (
              <article key={experience.id} className="relative border-l-2 pl-6">
                <div className="absolute -left-2 top-1 size-3 rounded-full border-2 border-background bg-primary" />

                <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
                  <div className="min-w-0">
                    <h3 className="font-semibold">{experience.job_title}</h3>

                    <p className="font-medium text-primary">
                      {experience.company}
                    </p>

                    <p className="text-sm text-muted-foreground">
                      {experience.location && `${experience.location} · `}

                      {experience.employment_type
                        .toLowerCase()
                        .replace('_', ' ')}

                      {' · '}

                      {experience.start_date}

                      {' - '}

                      {experience.is_current ? 'Present' : experience.end_date}
                    </p>
                  </div>

                  <div className="flex gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setEditingExperience(experience)}
                    >
                      <Pencil />
                      Edit
                    </Button>

                    <Button
                      variant="destructive"
                      size="sm"
                      disabled={deleteMutation.isPending}
                      onClick={() => handleDelete(experience)}
                    >
                      <Trash2 />
                      Delete
                    </Button>
                  </div>
                </div>

                {experience.description && (
                  <p className="mt-4 whitespace-pre-wrap text-sm text-muted-foreground">
                    {experience.description}
                  </p>
                )}

                {deleteMutation.isError &&
                  deleteMutation.variables?.experienceId === experience.id && (
                    <p className="mt-2 text-sm text-destructive">
                      {getApiErrorMessage(deleteMutation.error)}
                    </p>
                  )}
              </article>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  )
}

export default ExperienceSection
