import { zodResolver } from '@hookform/resolvers/zod'
import { Sparkles } from 'lucide-react'
import { useForm } from 'react-hook-form'

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
import { Textarea } from '@/components/ui/textarea'
import { useGenerateCoverLetter } from '@/features/ai/hooks/use_cover_letters'
import {
  coverLetterGenerationSchema,
  type CoverLetterGenerationFormValues,
} from '@/features/ai/schemas/cover_letter_schemas'
import type {
  CoverLetter,
  CoverLetterGenerationRequest,
} from '@/features/ai/types'
import { getApiErrorMessage } from '@/utils/api_error'

interface CoverLetterGenerationFormProps {
  resumeId: string
  onSuccess: (coverLetter: CoverLetter) => void
}

function CoverLetterGenerationForm({
  resumeId,
  onSuccess,
}: CoverLetterGenerationFormProps) {
  const generateMutation = useGenerateCoverLetter()

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<CoverLetterGenerationFormValues>({
    resolver: zodResolver(coverLetterGenerationSchema),
    defaultValues: {
      title: '',
      company_name: '',
      job_title: '',
      job_description: '',
    },
  })

  function onSubmit(values: CoverLetterGenerationFormValues) {
    const payload: CoverLetterGenerationRequest = {
      title: values.title.trim(),
      company_name: values.company_name.trim(),
      job_title: values.job_title.trim(),
      job_description: values.job_description.trim(),
    }

    generateMutation.mutate(
      {
        resumeId,
        payload,
      },
      {
        onSuccess,
      },
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Generate Cover Letter with AI</CardTitle>

        <CardDescription>
          Provide the target company, role, and job description to generate a
          tailored cover letter using your selected resume.
        </CardDescription>
      </CardHeader>

      <CardContent>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          <div className="grid gap-6 md:grid-cols-2">
            <div className="space-y-2">
              <Label htmlFor="title">Cover letter title</Label>

              <Input
                id="title"
                placeholder="e.g. Software Engineer Application"
                aria-invalid={Boolean(errors.title)}
                disabled={generateMutation.isPending}
                {...register('title')}
              />

              {errors.title && (
                <p className="text-sm text-destructive">
                  {errors.title.message}
                </p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="company_name">Company name</Label>

              <Input
                id="company_name"
                placeholder="e.g. Acme Technologies"
                aria-invalid={Boolean(errors.company_name)}
                disabled={generateMutation.isPending}
                {...register('company_name')}
              />

              {errors.company_name && (
                <p className="text-sm text-destructive">
                  {errors.company_name.message}
                </p>
              )}
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="job_title">Job title</Label>

            <Input
              id="job_title"
              placeholder="e.g. Backend Software Engineer"
              aria-invalid={Boolean(errors.job_title)}
              disabled={generateMutation.isPending}
              {...register('job_title')}
            />

            {errors.job_title && (
              <p className="text-sm text-destructive">
                {errors.job_title.message}
              </p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="job_description">Job description</Label>

            <Textarea
              id="job_description"
              rows={12}
              placeholder="Paste the job description here..."
              aria-invalid={Boolean(errors.job_description)}
              disabled={generateMutation.isPending}
              {...register('job_description')}
            />

            {errors.job_description && (
              <p className="text-sm text-destructive">
                {errors.job_description.message}
              </p>
            )}

            <p className="text-xs text-muted-foreground">
              Include the responsibilities, qualifications, and requirements
              from the job posting for a more targeted result.
            </p>
          </div>

          {generateMutation.isError && (
            <div className="rounded-lg border border-destructive/30 bg-destructive/5 px-4 py-3">
              <p className="text-sm text-destructive">
                {getApiErrorMessage(generateMutation.error)}
              </p>
            </div>
          )}

          <div className="flex justify-end">
            <Button type="submit" disabled={generateMutation.isPending}>
              <Sparkles />

              {generateMutation.isPending
                ? 'Generating...'
                : 'Generate Cover Letter'}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  )
}

export default CoverLetterGenerationForm
