import { ChevronLeft, Pencil, Plus, Wrench, Trash2 } from 'lucide-react'
import { useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'

import { Button, buttonVariants } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'

import SkillForm from '@/features/resumes/components/SkillForm'
import {
  useCreateSkill,
  useDeleteSkill,
  useSkills,
  useUpdateSkill,
} from '@/features/resumes/hooks/use_skills'
import { useResume } from '@/features/resumes/hooks/use_resumes'
import type { Skill } from '@/features/resumes/types'
import type { SkillFormValues } from '@/features/resumes/schemas/skill_schemas'
import type { SkillLevel } from '@/types/resume'
import { getApiErrorMessage } from '@/utils/api_error'

const skillLevelLabels: Record<SkillLevel, string> = {
  beginner: 'Beginner',
  intermediate: 'Intermediate',
  advanced: 'Advanced',
  expert: 'Expert',
}

function SkillsManagement() {
  const { resumeId } = useParams<{
    resumeId: string
  }>()

  const navigate = useNavigate()

  const [isCreating, setIsCreating] = useState(false)

  const [editingSkill, setEditingSkill] = useState<Skill | null>(null)

  const {
    data: resume,
    isLoading: isResumeLoading,
    isError: isResumeError,
    error: resumeError,
  } = useResume(resumeId ?? '')

  const {
    data: skills = [],
    isLoading: isSkillsLoading,
    isError: isSkillsError,
    error: skillsError,
  } = useSkills(resumeId ?? '')

  const createMutation = useCreateSkill()
  const updateMutation = useUpdateSkill()
  const deleteMutation = useDeleteSkill()

  const isSubmitting = createMutation.isPending || updateMutation.isPending

  function handleCreate(values: SkillFormValues) {
    if (!resumeId) {
      return
    }

    createMutation.mutate(
      {
        resumeId,
        payload: values,
      },
      {
        onSuccess: () => {
          setIsCreating(false)
        },
      },
    )
  }

  function handleUpdate(values: SkillFormValues) {
    if (!editingSkill) {
      return
    }

    updateMutation.mutate(
      {
        skillId: editingSkill.id,
        payload: values,
      },
      {
        onSuccess: () => {
          setEditingSkill(null)
        },
      },
    )
  }

  function handleDelete(skill: Skill) {
    if (!resumeId) {
      return
    }

    const confirmed = window.confirm(
      `Are you sure you want to delete "${skill.name}" from this resume? This action cannot be undone.`,
    )

    if (!confirmed) {
      return
    }

    deleteMutation.mutate({
      skillId: skill.id,
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

  if (isResumeLoading || isSkillsLoading) {
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
                className="h-24 animate-pulse rounded-lg bg-muted"
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

  if (isSkillsError) {
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
            <CardTitle>Unable to load skills</CardTitle>

            <CardDescription>{getApiErrorMessage(skillsError)}</CardDescription>
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
            Skills
          </h2>

          <p className="mt-2 text-muted-foreground">
            Manage your technical and professional skills for{' '}
            <span className="font-medium text-foreground">{resume.title}</span>.
          </p>
        </div>

        {!isCreating && !editingSkill && (
          <Button onClick={() => setIsCreating(true)}>
            <Plus />
            Add Skill
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
        <SkillForm
          isSubmitting={isSubmitting}
          onSubmit={handleCreate}
          onCancel={() => setIsCreating(false)}
        />
      )}

      {editingSkill && (
        <SkillForm
          skill={editingSkill}
          isSubmitting={isSubmitting}
          onSubmit={handleUpdate}
          onCancel={() => setEditingSkill(null)}
        />
      )}

      {!isCreating && !editingSkill && (
        <Card>
          <CardHeader>
            <div className="flex items-center gap-3">
              <Wrench className="size-6 text-primary" />

              <div>
                <CardTitle>Professional Skills</CardTitle>

                <CardDescription>
                  Add the technical and professional skills that demonstrate
                  your capabilities.
                </CardDescription>
              </div>
            </div>
          </CardHeader>

          <CardContent>
            {skills.length === 0 ? (
              <div className="flex flex-col items-center justify-center rounded-lg border border-dashed p-10 text-center">
                <Wrench className="size-10 text-muted-foreground" />

                <h3 className="mt-4 font-semibold">No skills added yet</h3>

                <p className="mt-2 max-w-md text-sm text-muted-foreground">
                  Add your technical and professional skills to showcase your
                  capabilities to potential employers.
                </p>

                <Button className="mt-6" onClick={() => setIsCreating(true)}>
                  <Plus />
                  Add your first skill
                </Button>
              </div>
            ) : (
              <div className="space-y-4">
                {skills.map((skill) => (
                  <SkillCard
                    key={skill.id}
                    skill={skill}
                    isDeleting={
                      deleteMutation.isPending &&
                      deleteMutation.variables?.skillId === skill.id
                    }
                    onEdit={() => setEditingSkill(skill)}
                    onDelete={() => handleDelete(skill)}
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

interface SkillCardProps {
  skill: Skill
  isDeleting: boolean
  onEdit: () => void
  onDelete: () => void
}

function SkillCard({ skill, isDeleting, onEdit, onDelete }: SkillCardProps) {
  return (
    <div className="rounded-lg border p-5">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div className="min-w-0">
          <h3 className="text-lg font-semibold">{skill.name}</h3>

          <p className="mt-1 text-sm text-muted-foreground">
            Proficiency:{' '}
            <span className="font-medium text-foreground">
              {skillLevelLabels[skill.proficiency]}
            </span>
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
    </div>
  )
}

export default SkillsManagement
