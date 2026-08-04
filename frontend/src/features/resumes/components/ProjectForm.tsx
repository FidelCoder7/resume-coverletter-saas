import { useEffect } from 'react'
import { useForm, useWatch } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'

import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'

import {
  projectSchema,
  type ProjectFormInput,
  type ProjectFormValues,
} from '@/features/resumes/schemas/project_schemas'

import type { Project } from '@/features/resumes/types'

interface ProjectFormProps {
  project?: Project
  isSubmitting?: boolean
  onSubmit: (values: ProjectFormValues) => void
  onCancel: () => void
}

function ProjectForm({
  project,
  isSubmitting = false,
  onSubmit,
  onCancel,
}: ProjectFormProps) {
  const form = useForm<ProjectFormInput, undefined, ProjectFormValues>({
    resolver: zodResolver(projectSchema),
    defaultValues: {
      name: project?.name ?? '',
      description: project?.description ?? '',
      technologies: project?.technologies ?? '',
      project_url: project?.project_url ?? '',
      repository_url: project?.repository_url ?? '',
      start_date: project?.start_date ?? '',
      end_date: project?.end_date ?? '',
      is_ongoing: project?.is_ongoing ?? false,
      display_order: project?.display_order ?? 0,
    },
  })

  const isOngoing = useWatch({
    control: form.control,
    name: 'is_ongoing',
  })

  useEffect(() => {
    if (isOngoing) {
      form.setValue('end_date', '')
    }
  }, [isOngoing, form])

  const errors = form.formState.errors

  return (
    <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
      <div className="grid gap-4 sm:grid-cols-2">
        <div className="space-y-2">
          <label htmlFor="name" className="text-sm font-medium">
            Project Name
          </label>

          <Input
            id="name"
            {...form.register('name')}
            placeholder="AI Resume & Cover Letter SaaS"
          />

          {errors.name && (
            <p className="text-sm text-destructive">{errors.name.message}</p>
          )}
        </div>

        <div className="space-y-2">
          <label htmlFor="technologies" className="text-sm font-medium">
            Technologies
          </label>

          <Input
            id="technologies"
            {...form.register('technologies')}
            placeholder="Python, FastAPI, React, PostgreSQL"
          />

          {errors.technologies && (
            <p className="text-sm text-destructive">
              {errors.technologies.message}
            </p>
          )}
        </div>
      </div>

      <div className="space-y-2">
        <label htmlFor="description" className="text-sm font-medium">
          Description
        </label>

        <Textarea
          id="description"
          {...form.register('description')}
          placeholder="Describe the project, your role, and the main outcomes."
          rows={5}
        />

        {errors.description && (
          <p className="text-sm text-destructive">
            {errors.description.message}
          </p>
        )}
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <div className="space-y-2">
          <label htmlFor="project_url" className="text-sm font-medium">
            Live Project URL
          </label>

          <Input
            id="project_url"
            type="url"
            {...form.register('project_url')}
            placeholder="https://example.com"
          />

          {errors.project_url && (
            <p className="text-sm text-destructive">
              {errors.project_url.message}
            </p>
          )}
        </div>

        <div className="space-y-2">
          <label htmlFor="repository_url" className="text-sm font-medium">
            Repository URL
          </label>

          <Input
            id="repository_url"
            type="url"
            {...form.register('repository_url')}
            placeholder="https://github.com/user/project"
          />

          {errors.repository_url && (
            <p className="text-sm text-destructive">
              {errors.repository_url.message}
            </p>
          )}
        </div>
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <div className="space-y-2">
          <label htmlFor="start_date" className="text-sm font-medium">
            Start Date
          </label>

          <Input id="start_date" type="date" {...form.register('start_date')} />

          {errors.start_date && (
            <p className="text-sm text-destructive">
              {errors.start_date.message}
            </p>
          )}
        </div>

        <div className="space-y-2">
          <label htmlFor="end_date" className="text-sm font-medium">
            End Date
          </label>

          <Input
            id="end_date"
            type="date"
            disabled={isOngoing}
            {...form.register('end_date')}
          />

          {errors.end_date && (
            <p className="text-sm text-destructive">
              {errors.end_date.message}
            </p>
          )}
        </div>
      </div>

      <label className="flex items-center gap-2 text-sm font-medium">
        <input
          type="checkbox"
          {...form.register('is_ongoing')}
          className="size-4 rounded border"
        />
        This project is ongoing
      </label>

      <div className="space-y-2">
        <label htmlFor="display_order" className="text-sm font-medium">
          Display Order
        </label>

        <Input
          id="display_order"
          type="number"
          min={0}
          {...form.register('display_order', {
            valueAsNumber: true,
          })}
        />

        {errors.display_order && (
          <p className="text-sm text-destructive">
            {errors.display_order.message}
          </p>
        )}
      </div>

      <div className="flex justify-end gap-2">
        <Button
          type="button"
          variant="outline"
          onClick={onCancel}
          disabled={isSubmitting}
        >
          Cancel
        </Button>

        <Button type="submit" disabled={isSubmitting}>
          {isSubmitting
            ? 'Saving...'
            : project
              ? 'Update Project'
              : 'Add Project'}
        </Button>
      </div>
    </form>
  )
}

export default ProjectForm
