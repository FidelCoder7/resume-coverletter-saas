import { zodResolver } from '@hookform/resolvers/zod'
import { ArrowLeft, Save } from 'lucide-react'
import { useForm } from 'react-hook-form'
import { Link, useNavigate } from 'react-router-dom'

import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { useCreateResume } from '@/features/resumes/hooks/use_resumes'
import {
  createResumeSchema,
  type CreateResumeFormValues,
} from '@/features/resumes/schemas/resume_schemas'
import { getApiErrorMessage } from '@/utils/api_error'
import { buttonVariants } from '@/components/ui/button'

function CreateResume() {
  const navigate = useNavigate()
  const createMutation = useCreateResume()

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<CreateResumeFormValues>({
    resolver: zodResolver(createResumeSchema),
    defaultValues: {
      title: '',
      summary: '',
    },
  })

  function onSubmit(values: CreateResumeFormValues) {
    createMutation.mutate(
      {
        title: values.title.trim(),
        summary: values.summary?.trim() || null,
      },
      {
        onSuccess: (resume) => {
          navigate(`/resumes/${resume.id}/edit`)
        },
      },
    )
  }

  return (
    <div className="mx-auto w-full max-w-3xl space-y-6">
      <div>
        <Link to="/resumes" className={buttonVariants({ variant: 'outline' })}>
          <ArrowLeft />
          Back to resumes
        </Link>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Create a Resume</CardTitle>

          <CardDescription>
            Start with a title and professional summary. You can add your
            experience, education, skills, projects, and certifications next.
          </CardDescription>
        </CardHeader>

        <CardContent>
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="title">Resume title</Label>

              <Input
                id="title"
                placeholder="e.g. Software Engineer Resume"
                aria-invalid={Boolean(errors.title)}
                {...register('title')}
              />

              {errors.title && (
                <p className="text-sm text-destructive">
                  {errors.title.message}
                </p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="summary">Professional summary</Label>

              <textarea
                id="summary"
                rows={7}
                placeholder="Write a concise summary of your professional background, skills, and career goals."
                aria-invalid={Boolean(errors.summary)}
                className="flex min-h-20 w-full rounded-lg border border-input bg-transparent px-3 py-2 text-sm transition-colors outline-none placeholder:text-muted-foreground focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/50 aria-invalid:border-destructive aria-invalid:ring-3 aria-invalid:ring-destructive/20"
                {...register('summary')}
              />

              {errors.summary && (
                <p className="text-sm text-destructive">
                  {errors.summary.message}
                </p>
              )}
            </div>

            {createMutation.isError && (
              <p className="text-sm text-destructive">
                {getApiErrorMessage(createMutation.error)}
              </p>
            )}

            <div className="flex justify-end gap-3">
              <Link
                to="/resumes"
                className={buttonVariants({ variant: 'outline' })}
              >
                Cancel
              </Link>

              <Button type="submit" disabled={createMutation.isPending}>
                <Save />
                {createMutation.isPending ? 'Creating...' : 'Create Resume'}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}

export default CreateResume
