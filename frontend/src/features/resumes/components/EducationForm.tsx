import { zodResolver } from '@hookform/resolvers/zod'
import { Loader2 } from 'lucide-react'
import { useEffect } from 'react'
import { useForm, useWatch } from 'react-hook-form'

import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

import {
  educationSchema,
  type EducationFormValues,
} from '@/features/resumes/schemas/education_schemas'

import type { Education } from '@/features/resumes/types'

interface EducationFormProps {
  education?: Education
  isSubmitting: boolean
  onSubmit: (values: EducationFormValues) => void
  onCancel: () => void
}

function EducationForm({
  education,
  isSubmitting,
  onSubmit,
  onCancel,
}: EducationFormProps) {
  const form = useForm<EducationFormValues>({
    resolver: zodResolver(educationSchema),
    defaultValues: {
      institution: education?.institution ?? '',
      degree: education?.degree ?? '',
      field_of_study: education?.field_of_study ?? '',
      location: education?.location ?? '',
      grade: education?.grade ?? '',
      start_date: education?.start_date ?? '',
      end_date: education?.end_date ?? '',
      is_current: education?.is_current ?? false,
      description: education?.description ?? '',
      display_order: education?.display_order ?? 0,
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

  function handleSubmit(values: EducationFormValues) {
    onSubmit(values)
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>{education ? 'Edit Education' : 'Add Education'}</CardTitle>
      </CardHeader>

      <CardContent>
        <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-6">
          <div className="grid gap-6 md:grid-cols-2">
            <div className="space-y-2">
              <Label htmlFor="institution">Institution</Label>

              <Input
                id="institution"
                {...form.register('institution')}
                disabled={isSubmitting}
                placeholder="University of Nairobi"
              />

              {form.formState.errors.institution && (
                <p className="text-sm text-destructive">
                  {form.formState.errors.institution.message}
                </p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="degree">Degree</Label>

              <Input
                id="degree"
                {...form.register('degree')}
                disabled={isSubmitting}
                placeholder="Bachelor of Science"
              />

              {form.formState.errors.degree && (
                <p className="text-sm text-destructive">
                  {form.formState.errors.degree.message}
                </p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="field_of_study">Field of Study</Label>

              <Input
                id="field_of_study"
                {...form.register('field_of_study')}
                disabled={isSubmitting}
                placeholder="Computer Science"
              />

              {form.formState.errors.field_of_study && (
                <p className="text-sm text-destructive">
                  {form.formState.errors.field_of_study.message}
                </p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="location">Location</Label>

              <Input
                id="location"
                {...form.register('location')}
                disabled={isSubmitting}
                placeholder="Nairobi, Kenya"
              />

              {form.formState.errors.location && (
                <p className="text-sm text-destructive">
                  {form.formState.errors.location.message}
                </p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="grade">Grade</Label>

              <Input
                id="grade"
                {...form.register('grade')}
                disabled={isSubmitting}
                placeholder="Second Class Upper"
              />

              {form.formState.errors.grade && (
                <p className="text-sm text-destructive">
                  {form.formState.errors.grade.message}
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
            I am currently studying here
          </label>

          <div className="space-y-2">
            <Label htmlFor="description">Description</Label>

            <textarea
              id="description"
              rows={6}
              {...form.register('description')}
              disabled={isSubmitting}
              className="flex min-h-24 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
              placeholder="Describe your studies, achievements, relevant coursework, or activities..."
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

            {form.formState.errors.display_order && (
              <p className="text-sm text-destructive">
                {form.formState.errors.display_order.message}
              </p>
            )}
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

              {education ? 'Save Changes' : 'Add Education'}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  )
}

export default EducationForm
