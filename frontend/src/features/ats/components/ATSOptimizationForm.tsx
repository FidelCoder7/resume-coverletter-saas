import { zodResolver } from '@hookform/resolvers/zod'
import { SearchCheck } from 'lucide-react'
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
import { useOptimizeResumeForATS } from '@/features/ats/hooks/use_ats'
import {
  atsOptimizationSchema,
  type ATSOptimizationFormValues,
} from '@/features/ats/schemas/ats_schemas'
import type {
  ATSOptimizationRequest,
  ATSOptimizationResponse,
} from '@/features/ats/types'
import { getApiErrorMessage } from '@/utils/api_error'

interface ATSOptimizationFormProps {
  resumeId: string
  onSuccess: (result: ATSOptimizationResponse) => void
}

function ATSOptimizationForm({
  resumeId,
  onSuccess,
}: ATSOptimizationFormProps) {
  const optimizeMutation = useOptimizeResumeForATS()

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ATSOptimizationFormValues>({
    resolver: zodResolver(atsOptimizationSchema),
    defaultValues: {
      target_job_title: '',
      job_description: '',
    },
  })

  function onSubmit(values: ATSOptimizationFormValues) {
    const payload: ATSOptimizationRequest = {
      job_description: values.job_description.trim(),
      target_job_title: values.target_job_title?.trim() || null,
    }

    optimizeMutation.mutate(
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
        <CardTitle>Optimize Resume for ATS</CardTitle>

        <CardDescription>
          Compare your resume against a target job description to identify
          keywords and improvements that can strengthen ATS compatibility.
        </CardDescription>
      </CardHeader>

      <CardContent>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="target_job_title">Target job title</Label>

            <Input
              id="target_job_title"
              placeholder="e.g. Backend Software Engineer"
              aria-invalid={Boolean(errors.target_job_title)}
              disabled={optimizeMutation.isPending}
              {...register('target_job_title')}
            />

            {errors.target_job_title && (
              <p className="text-sm text-destructive">
                {errors.target_job_title.message}
              </p>
            )}

            <p className="text-xs text-muted-foreground">
              Optional. Specify the role you are targeting to make the analysis
              more focused.
            </p>
          </div>

          <div className="space-y-2">
            <Label htmlFor="job_description">Job description</Label>

            <Textarea
              id="job_description"
              rows={14}
              placeholder="Paste the target job description here..."
              aria-invalid={Boolean(errors.job_description)}
              disabled={optimizeMutation.isPending}
              {...register('job_description')}
            />

            {errors.job_description && (
              <p className="text-sm text-destructive">
                {errors.job_description.message}
              </p>
            )}

            <p className="text-xs text-muted-foreground">
              Include the responsibilities, qualifications, technologies, and
              other requirements from the job posting.
            </p>
          </div>

          {optimizeMutation.isError && (
            <div className="rounded-lg border border-destructive/30 bg-destructive/5 px-4 py-3">
              <p className="text-sm text-destructive">
                {getApiErrorMessage(optimizeMutation.error)}
              </p>
            </div>
          )}

          <div className="flex justify-end">
            <Button type="submit" disabled={optimizeMutation.isPending}>
              <SearchCheck />

              {optimizeMutation.isPending ? 'Analyzing...' : 'Optimize Resume'}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  )
}

export default ATSOptimizationForm
