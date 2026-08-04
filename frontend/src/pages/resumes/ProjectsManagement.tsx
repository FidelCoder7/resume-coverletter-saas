import { ExternalLink, GitBranch, Pencil, Plus, Trash2 } from 'lucide-react'
import { useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import { Button, buttonVariants } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'

import ProjectForm from '@/features/resumes/components/ProjectForm'
import {
  useCreateProject,
  useDeleteProject,
  useProjects,
  useUpdateProject,
} from '@/features/resumes/hooks/use_projects'

import type { Project } from '@/features/resumes/types'
import type { ProjectFormValues } from '@/features/resumes/schemas/project_schemas'

import { getApiErrorMessage } from '@/utils/api_error'

function ProjectsManagement() {
  const { resumeId } = useParams<{ resumeId: string }>()

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
        </Card>
      </div>
    )
  }

  return <ProjectsManagementContent resumeId={resumeId} />
}

interface ProjectsManagementContentProps {
  resumeId: string
}

function ProjectsManagementContent({
  resumeId,
}: ProjectsManagementContentProps) {
  const [editingProject, setEditingProject] = useState<Project | null>(null)
  const [isCreating, setIsCreating] = useState(false)

  const {
    data: projects = [],
    isLoading,
    isError,
    error,
  } = useProjects(resumeId ?? '')

  const createMutation = useCreateProject()
  const updateMutation = useUpdateProject()
  const deleteMutation = useDeleteProject()

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
        </Card>
      </div>
    )
  }

  function handleCreate(values: ProjectFormValues) {
    createMutation.mutate(
      {
        resumeId,
        payload: {
          ...values,
          project_url: values.project_url || null,
          repository_url: values.repository_url || null,
          start_date: values.start_date || null,
          end_date: values.end_date || null,
        },
      },
      {
        onSuccess: () => {
          setIsCreating(false)
        },
      },
    )
  }

  function handleUpdate(values: ProjectFormValues) {
    if (!editingProject) {
      return
    }

    updateMutation.mutate(
      {
        projectId: editingProject.id,
        resumeId,
        payload: {
          ...values,
          project_url: values.project_url || null,
          repository_url: values.repository_url || null,
          start_date: values.start_date || null,
          end_date: values.end_date || null,
        },
      },
      {
        onSuccess: () => {
          setEditingProject(null)
        },
      },
    )
  }

  function handleDelete(project: Project) {
    const confirmed = window.confirm(
      `Are you sure you want to delete "${project.name}"? This action cannot be undone.`,
    )

    if (!confirmed) {
      return
    }

    deleteMutation.mutate({
      projectId: project.id,
      resumeId,
    })
  }

  if (isLoading) {
    return (
      <div className="mx-auto w-full max-w-7xl space-y-6">
        <div className="h-8 w-64 animate-pulse rounded bg-muted" />

        <div className="grid gap-4">
          <div className="h-40 animate-pulse rounded-lg bg-muted" />
          <div className="h-40 animate-pulse rounded-lg bg-muted" />
        </div>
      </div>
    )
  }

  if (isError) {
    return (
      <div className="mx-auto w-full max-w-7xl">
        <Card>
          <CardHeader>
            <CardTitle>Unable to load projects</CardTitle>
            <CardDescription>{getApiErrorMessage(error)}</CardDescription>
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
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <Link
            to={`/resumes/${resumeId}`}
            className={buttonVariants({ variant: 'outline' })}
          >
            Back to Resume
          </Link>

          <h1 className="mt-6 text-2xl font-semibold tracking-tight sm:text-3xl">
            Projects
          </h1>

          <p className="mt-2 text-muted-foreground">
            Showcase your projects, technologies, and technical achievements.
          </p>
        </div>

        {!isCreating && !editingProject && (
          <Button onClick={() => setIsCreating(true)}>
            <Plus />
            Add Project
          </Button>
        )}
      </div>

      {(isCreating || editingProject) && (
        <Card>
          <CardHeader>
            <CardTitle>
              {editingProject ? 'Edit Project' : 'Add Project'}
            </CardTitle>

            <CardDescription>
              {editingProject
                ? 'Update the project information on your resume.'
                : 'Add a project to showcase on your resume.'}
            </CardDescription>
          </CardHeader>

          <CardContent>
            <ProjectForm
              project={editingProject ?? undefined}
              isSubmitting={
                createMutation.isPending || updateMutation.isPending
              }
              onSubmit={editingProject ? handleUpdate : handleCreate}
              onCancel={() => {
                setIsCreating(false)
                setEditingProject(null)
              }}
            />

            {(createMutation.isError || updateMutation.isError) && (
              <p className="mt-4 text-sm text-destructive">
                {getApiErrorMessage(
                  createMutation.error || updateMutation.error,
                )}
              </p>
            )}
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

      {projects.length === 0 ? (
        <Card>
          <CardHeader>
            <CardTitle>No projects yet</CardTitle>

            <CardDescription>
              Add your first project to start building your resume.
            </CardDescription>
          </CardHeader>

          <CardContent>
            {!isCreating && (
              <Button onClick={() => setIsCreating(true)}>
                <Plus />
                Add Your First Project
              </Button>
            )}
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-4">
          {projects.map((project) => (
            <Card key={project.id}>
              <CardHeader>
                <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
                  <div className="min-w-0">
                    <CardTitle>{project.name}</CardTitle>

                    <CardDescription className="mt-2">
                      {project.technologies}
                    </CardDescription>
                  </div>

                  <div className="flex shrink-0 gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => {
                        setEditingProject(project)
                        setIsCreating(false)
                      }}
                    >
                      <Pencil />
                      Edit
                    </Button>

                    <Button
                      variant="destructive"
                      size="sm"
                      disabled={deleteMutation.isPending}
                      onClick={() => handleDelete(project)}
                    >
                      <Trash2 />
                      Delete
                    </Button>
                  </div>
                </div>
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

                <div className="flex flex-wrap gap-4 text-sm text-muted-foreground">
                  {project.start_date && (
                    <span>
                      Started{' '}
                      {new Date(project.start_date).toLocaleDateString()}
                    </span>
                  )}

                  {project.is_ongoing ? (
                    <span>Ongoing</span>
                  ) : (
                    project.end_date && (
                      <span>
                        Ended {new Date(project.end_date).toLocaleDateString()}
                      </span>
                    )
                  )}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}

export default ProjectsManagement
