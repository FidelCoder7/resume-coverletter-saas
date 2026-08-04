import { ArrowLeft, Save } from 'lucide-react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'

import { Button, buttonVariants } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
  useResume,
  useUpdateResume,
} from '@/features/resumes/hooks/use_resumes'
import {
  updateResumeSchema,
  type UpdateResumeFormValues,
} from '@/features/resumes/schemas/resume_schemas'
import { getApiErrorMessage } from '@/utils/api_error'

function EditResume() {
  const { resumeId } = useParams<{ resumeId: string }>()
  const navigate = useNavigate()

  const { data: resume, isLoading, isError, error } = useResume(resumeId ?? '')

  const updateMutation = useUpdateResume()

  const form = useForm<UpdateResumeFormValues>({
    resolver: zodResolver(updateResumeSchema),
    values: {
      title: resume?.title ?? '',
      summary: resume?.summary ?? '',
    },
  })

  function onSubmit(values: UpdateResumeFormValues) {
    if (!resumeId) {
      return
    }

    updateMutation.mutate(
      {
        resumeId,
        payload: {
          title: values.title.trim(),
          summary: values.summary?.trim() || null,
        },
      },
      {
        onSuccess: () => {
          navigate(`/resumes/${resumeId}`)
        },
      },
    )
  }

  if (!resumeId) {
    return (
      <div className="mx-auto w-full max-w-3xl">
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
      <div className="mx-auto w-full max-w-3xl">
        <Card>
          <CardHeader>
            <div className="h-7 w-1/2 animate-pulse rounded bg-muted" />

            <div className="h-4 w-3/4 animate-pulse rounded bg-muted" />
          </CardHeader>

          <CardContent className="space-y-6">
            <div className="h-8 w-full animate-pulse rounded bg-muted" />

            <div className="h-32 w-full animate-pulse rounded bg-muted" />
          </CardContent>
        </Card>
      </div>
    )
  }

  if (isError || !resume) {
    return (
      <div className="mx-auto w-full max-w-3xl">
        <Card>
          <CardHeader>
            <CardTitle>Unable to load resume</CardTitle>

            <CardDescription>{getApiErrorMessage(error)}</CardDescription>
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

  return (
    <div className="mx-auto w-full max-w-3xl space-y-6">
      <div>
        <Link to={`/resumes/${resume.id}`}>
          className={buttonVariants({ variant: 'outline' })}
          <ArrowLeft />
          Back to resume Manager
        </Link>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Edit Resume Details</CardTitle>

          <CardDescription>
            Update the title and professional summary for this resume.
          </CardDescription>
        </CardHeader>

        <CardContent>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="title">Resume Title</Label>

              <Input
                id="title"
                placeholder="e.g. Software Engineer Resume"
                {...form.register('title')}
                aria-invalid={Boolean(form.formState.errors.title)}
              />

              {form.formState.errors.title && (
                <p className="text-sm text-destructive">
                  {form.formState.errors.title.message}
                </p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="summary">Professional Summary</Label>

              <textarea
                id="summary"
                rows={8}
                placeholder="Write a concise professional summary..."
                {...form.register('summary')}
                className="w-full rounded-lg border border-input bg-transparent px-3 py-2 text-sm outline-none transition-colors placeholder:text-muted-foreground focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/50"
                aria-invalid={Boolean(form.formState.errors.summary)}
              />

              {form.formState.errors.summary && (
                <p className="text-sm text-destructive">
                  {form.formState.errors.summary.message}
                </p>
              )}
            </div>

            {updateMutation.isError && (
              <p className="text-sm text-destructive">
                {getApiErrorMessage(updateMutation.error)}
              </p>
            )}

            <div className="flex flex-col-reverse gap-2 sm:flex-row sm:justify-end">
              <Button
                type="button"
                variant="outline"
                disabled={updateMutation.isPending}
                onClick={() => navigate(`/resumes/${resume.id}`)}
              >
                Cancel
              </Button>

              <Button type="submit" disabled={updateMutation.isPending}>
                <Save />

                {updateMutation.isPending ? 'Saving...' : 'Save Changes'}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}

export default EditResume
