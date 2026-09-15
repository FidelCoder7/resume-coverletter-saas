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
import { useGenerateResume } from '@/features/resumes/hooks/use_resumes'
import type { Resume, ResumeGenerationRequest } from '@/features/resumes/types'
import {
  resumeGenerationSchema,
  type ResumeGenerationFormValues,
} from '@/features/ai/schemas/resume_schemas'
import { getApiErrorMessage } from '@/utils/api_error'

interface ResumeGenerationFormProps {
  resumeId: string
  onSuccess: (resume: Resume) => void
}

function ResumeGenerationForm({
  resumeId,
  onSuccess,
}: ResumeGenerationFormProps) {
  const generateMutation = useGenerateResume()

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ResumeGenerationFormValues>({
    resolver: zodResolver(resumeGenerationSchema),
    defaultValues: {
      target_job_title: '',
      job_description: '',
    },
  })

  function onSubmit(values: ResumeGenerationFormValues) {
    const payload: ResumeGenerationRequest = {
      target_job_title: values.target_job_title?.trim() || null,
      job_description: values.job_description?.trim() || null,
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
        <CardTitle>Generate Resume with AI</CardTitle>

        <CardDescription>
          Provide a target role and job description to tailor your resume
          content for a specific opportunity.
        </CardDescription>
      </CardHeader>

      <CardContent>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="target_job_title">Target job title</Label>

            <Input
              id="target_job_title"
              placeholder="e.g. Software Engineer"
              aria-invalid={Boolean(errors.target_job_title)}
              disabled={generateMutation.isPending}
              {...register('target_job_title')}
            />

            {errors.target_job_title && (
              <p className="text-sm text-destructive">
                {errors.target_job_title.message}
              </p>
            )}

            <p className="text-xs text-muted-foreground">
              Optional. Use the role you are targeting to guide the AI.
            </p>
          </div>

          <div className="space-y-2">
            <Label htmlFor="job_description">Job description</Label>

            <Textarea
              id="job_description"
              rows={10}
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
              Optional, but recommended for a job-specific resume.
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

              {generateMutation.isPending ? 'Generating...' : 'Generate Resume'}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  )
}

export default ResumeGenerationForm
