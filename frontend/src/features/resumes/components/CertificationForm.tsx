import { useEffect } from 'react'
import { useForm, useWatch } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'

import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

import {
  certificationSchema,
  type CertificationFormValues,
} from '@/features/resumes/schemas/certification_schemas'

import type { Certification } from '@/features/resumes/types'

interface CertificationFormProps {
  certification?: Certification
  isSubmitting?: boolean
  onSubmit: (values: CertificationFormValues) => void
  onCancel: () => void
}

function CertificationForm({
  certification,
  isSubmitting = false,
  onSubmit,
  onCancel,
}: CertificationFormProps) {
  const form = useForm<CertificationFormValues>({
    resolver: zodResolver(certificationSchema),
    defaultValues: {
      name: certification?.name ?? '',
      issuing_organization: certification?.issuing_organization ?? '',
      credential_id: certification?.credential_id ?? '',
      credential_url: certification?.credential_url ?? '',
      issue_date: certification?.issue_date ?? '',
      expiration_date: certification?.expiration_date ?? '',
      does_not_expire: certification?.does_not_expire ?? false,
      display_order: certification?.display_order ?? 0,
    },
  })

  const doesNotExpire = useWatch({
    control: form.control,
    name: 'does_not_expire',
  })

  useEffect(() => {
    if (doesNotExpire) {
      form.setValue('expiration_date', '')
    }
  }, [doesNotExpire, form])

  const errors = form.formState.errors

  return (
    <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
      <div className="grid gap-4 sm:grid-cols-2">
        <div className="space-y-2">
          <label htmlFor="name" className="text-sm font-medium">
            Certification Name
          </label>

          <Input
            id="name"
            {...form.register('name')}
            placeholder="AWS Certified Cloud Practitioner"
          />

          {errors.name && (
            <p className="text-sm text-destructive">{errors.name.message}</p>
          )}
        </div>

        <div className="space-y-2">
          <label htmlFor="issuing_organization" className="text-sm font-medium">
            Issuing Organization
          </label>

          <Input
            id="issuing_organization"
            {...form.register('issuing_organization')}
            placeholder="Amazon Web Services"
          />

          {errors.issuing_organization && (
            <p className="text-sm text-destructive">
              {errors.issuing_organization.message}
            </p>
          )}
        </div>
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <div className="space-y-2">
          <label htmlFor="credential_id" className="text-sm font-medium">
            Credential ID
          </label>

          <Input
            id="credential_id"
            {...form.register('credential_id')}
            placeholder="ABC123456"
          />

          {errors.credential_id && (
            <p className="text-sm text-destructive">
              {errors.credential_id.message}
            </p>
          )}
        </div>

        <div className="space-y-2">
          <label htmlFor="credential_url" className="text-sm font-medium">
            Credential URL
          </label>

          <Input
            id="credential_url"
            type="url"
            {...form.register('credential_url')}
            placeholder="https://example.com/verify"
          />

          {errors.credential_url && (
            <p className="text-sm text-destructive">
              {errors.credential_url.message}
            </p>
          )}
        </div>
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <div className="space-y-2">
          <label htmlFor="issue_date" className="text-sm font-medium">
            Issue Date
          </label>

          <Input id="issue_date" type="date" {...form.register('issue_date')} />

          {errors.issue_date && (
            <p className="text-sm text-destructive">
              {errors.issue_date.message}
            </p>
          )}
        </div>

        <div className="space-y-2">
          <label htmlFor="expiration_date" className="text-sm font-medium">
            Expiration Date
          </label>

          <Input
            id="expiration_date"
            type="date"
            disabled={doesNotExpire}
            {...form.register('expiration_date')}
          />

          {errors.expiration_date && (
            <p className="text-sm text-destructive">
              {errors.expiration_date.message}
            </p>
          )}
        </div>
      </div>

      <label className="flex items-center gap-2 text-sm font-medium">
        <input
          type="checkbox"
          {...form.register('does_not_expire')}
          className="size-4 rounded border"
        />
        This certification does not expire
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
            : certification
              ? 'Update Certification'
              : 'Add Certification'}
        </Button>
      </div>
    </form>
  )
}

export default CertificationForm
