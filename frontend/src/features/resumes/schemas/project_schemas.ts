import { z } from 'zod'

const optionalUrl = z
  .string()
  .trim()
  .url('Enter a valid URL.')
  .or(z.literal(''))

export const projectSchema = z
  .object({
    name: z
      .string()
      .trim()
      .min(1, 'Project name is required.')
      .max(200, 'Project name must be 200 characters or fewer.'),

    description: z.string().trim().min(1, 'Project description is required.'),

    technologies: z.string().trim().min(1, 'Technologies are required.'),

    project_url: optionalUrl,

    repository_url: optionalUrl,

    start_date: z.string(),

    end_date: z.string(),

    is_ongoing: z.boolean(),

    display_order: z.coerce
      .number()
      .int('Display order must be a whole number.')
      .min(0, 'Display order cannot be negative.'),
  })
  .superRefine((data, context) => {
    if (data.is_ongoing && data.end_date) {
      context.addIssue({
        code: z.ZodIssueCode.custom,
        path: ['end_date'],
        message: 'Ongoing projects cannot have an end date.',
      })
    }

    if (data.start_date && data.end_date && data.end_date < data.start_date) {
      context.addIssue({
        code: z.ZodIssueCode.custom,
        path: ['end_date'],
        message: 'End date cannot be earlier than start date.',
      })
    }
  })

export type ProjectFormInput = z.input<typeof projectSchema>
export type ProjectFormValues = z.infer<typeof projectSchema>
