import { zodResolver } from '@hookform/resolvers/zod'
import { Loader2 } from 'lucide-react'
import { useEffect } from 'react'
import { useForm, useWatch } from 'react-hook-form'

import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

import { EMPLOYMENT_TYPES } from '@/types/resume'

import {
  experienceSchema,
  type ExperienceFormValues,
} from '@/features/resumes/schemas/experience_schemas'

import type { Experience } from '@/features/resumes/types'

interface ExperienceFormProps {
  experience?: Experience
  isSubmitting: boolean
  onSubmit: (values: ExperienceFormValues) => void
  onCancel: () => void
}

function ExperienceForm({
  experience,
  isSubmitting,
  onSubmit,
  onCancel,
}: ExperienceFormProps) {
  const form = useForm<ExperienceFormValues>({
    resolver: zodResolver(experienceSchema),
    defaultValues: {
      company: experience?.company ?? '',
      job_title: experience?.job_title ?? '',
      location: experience?.location ?? '',
      employment_type: experience?.employment_type ?? EMPLOYMENT_TYPES[0],
      start_date: experience?.start_date ?? '',
      end_date: experience?.end_date ?? '',
      is_current: experience?.is_current ?? false,
      description: experience?.description ?? '',
      display_order: experience?.display_order ?? 0,
    },
  })

  const isCurrent = useWatch({
    control: form.control,
    name: 'is_current',
  })

  useEffect(() => {
    if (isCurrent) {
      form.setValue('end_date', '')
      form.clearErrors('end_date')
    }
  }, [isCurrent, form])

  function handleSubmit(values: ExperienceFormValues) {
    onSubmit(values)
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>
          {experience ? 'Edit Experience' : 'Add Experience'}
        </CardTitle>
      </CardHeader>

      <CardContent>
        <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-6">
          <div className="grid gap-6 md:grid-cols-2">
            <div className="space-y-2">
              <Label htmlFor="company">Company</Label>

              <Input
                id="company"
                {...form.register('company')}
                disabled={isSubmitting}
              />

              {form.formState.errors.company && (
                <p className="text-sm text-destructive">
                  {form.formState.errors.company.message}
                </p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="job_title">Job Title</Label>

              <Input
                id="job_title"
                {...form.register('job_title')}
                disabled={isSubmitting}
              />

              {form.formState.errors.job_title && (
                <p className="text-sm text-destructive">
                  {form.formState.errors.job_title.message}
                </p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="location">Location</Label>

              <Input
                id="location"
                placeholder="Nairobi, Kenya"
                {...form.register('location')}
                disabled={isSubmitting}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="employment_type">Employment Type</Label>

              <select
                id="employment_type"
                {...form.register('employment_type')}
                disabled={isSubmitting}
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
              >
                {EMPLOYMENT_TYPES.map((type) => (
                  <option key={type} value={type}>
                    {type.toLowerCase().replace('_', ' ')}
                  </option>
                ))}
              </select>

              {form.formState.errors.employment_type && (
                <p className="text-sm text-destructive">
                  {form.formState.errors.employment_type.message}
                </p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="start_date">Start Date</Label>

              <Input
                id="start_date"
                type="date"
                {...form.register('start_date')}
                disabled={isSubmitting}
              />

              {form.formState.errors.start_date && (
                <p className="text-sm text-destructive">
                  {form.formState.errors.start_date.message}
                </p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="end_date">End Date</Label>

              <Input
                id="end_date"
                type="date"
                {...form.register('end_date')}
                disabled={isSubmitting || isCurrent}
              />

              {form.formState.errors.end_date && (
                <p className="text-sm text-destructive">
                  {form.formState.errors.end_date.message}
                </p>
              )}
            </div>
          </div>

          <label className="flex items-center gap-2 text-sm">
            <input
              type="checkbox"
              {...form.register('is_current')}
              disabled={isSubmitting}
              className="size-4"
            />
            I currently work here
          </label>

          <div className="space-y-2">
            <Label htmlFor="description">Description</Label>

            <textarea
              id="description"
              rows={6}
              {...form.register('description')}
              disabled={isSubmitting}
              className="flex min-h-24 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
              placeholder="Describe your responsibilities, achievements, and impact..."
            />

            {form.formState.errors.description && (
              <p className="text-sm text-destructive">
                {form.formState.errors.description.message}
              </p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="display_order">Display Order</Label>

            <Input
              id="display_order"
              type="number"
              min={0}
              {...form.register('display_order', {
                valueAsNumber: true,
              })}
              disabled={isSubmitting}
            />
          </div>

          <div className="flex justify-end gap-3">
            <Button
              type="button"
              variant="outline"
              onClick={onCancel}
              disabled={isSubmitting}
            >
              Cancel
            </Button>

            <Button type="submit" disabled={isSubmitting}>
              {isSubmitting && <Loader2 className="animate-spin" />}

              {experience ? 'Save Changes' : 'Add Experience'}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  )
}

export default ExperienceForm
