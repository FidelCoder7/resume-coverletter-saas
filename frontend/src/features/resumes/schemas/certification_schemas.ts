import { z } from 'zod'

export const certificationSchema = z
  .object({
    name: z
      .string()
      .trim()
      .min(1, 'Certification name is required.')
      .max(200, 'Certification name must be less than 200 characters.'),

    issuing_organization: z
      .string()
      .trim()
      .min(1, 'Issuing organization is required.')
      .max(200, 'Issuing organization must be less than 200 characters.'),

    credential_id: z
      .string()
      .trim()
      .max(200, 'Credential ID must be less than 200 characters.')
      .optional()
      .or(z.literal('')),

    credential_url: z
      .string()
      .trim()
      .url('Credential URL must be a valid URL.')
      .optional()
      .or(z.literal('')),

    issue_date: z.string().min(1, 'Issue date is required.'),

    expiration_date: z.string().optional().or(z.literal('')),

    does_not_expire: z.boolean(),

    display_order: z.number().int().min(0),
  })
  .superRefine((data, context) => {
    if (data.does_not_expire && data.expiration_date) {
      context.addIssue({
        code: 'custom',
        path: ['expiration_date'],
        message:
          'Expiration date must be empty for certifications that do not expire.',
      })
    }

    if (
      data.expiration_date &&
      data.issue_date &&
      data.expiration_date < data.issue_date
    ) {
      context.addIssue({
        code: 'custom',
        path: ['expiration_date'],
        message: 'Expiration date cannot be earlier than the issue date.',
      })
    }

    if (data.issue_date > new Date().toISOString().split('T')[0]) {
      context.addIssue({
        code: 'custom',
        path: ['issue_date'],
        message: 'Issue date cannot be in the future.',
      })
    }
  })

export type CertificationFormValues = z.infer<typeof certificationSchema>
