import { z } from 'zod'

export const educationSchema = z
  .object({
    institution: z
      .string()
      .trim()
      .min(1, 'Institution is required.')
      .max(255, 'Institution must be less than 255 characters.'),

    degree: z
      .string()
      .trim()
      .min(1, 'Degree is required.')
      .max(255, 'Degree must be less than 255 characters.'),

    field_of_study: z
      .string()
      .trim()
      .min(1, 'Field of study is required.')
      .max(255, 'Field of study must be less than 255 characters.'),

    location: z
      .string()
      .trim()
      .max(255, 'Location must be less than 255 characters.')
      .optional()
      .or(z.literal('')),

    grade: z
      .string()
      .trim()
      .max(100, 'Grade must be less than 100 characters.')
      .optional()
      .or(z.literal('')),

    start_date: z.string().min(1, 'Start date is required.'),

    end_date: z.string().optional().or(z.literal('')),

    is_current: z.boolean(),

    description: z.string().trim().optional().or(z.literal('')),

    display_order: z.number().int().min(0),
  })
  .superRefine((data, context) => {
    if (!data.is_current && !data.end_date) {
      context.addIssue({
        code: 'custom',
        path: ['end_date'],
        message: 'End date is required when this education is not current.',
      })
    }

    if (data.is_current && data.end_date) {
      context.addIssue({
        code: 'custom',
        path: ['end_date'],
        message: 'End date must be empty for current education.',
      })
    }

    if (data.end_date && data.start_date && data.end_date < data.start_date) {
      context.addIssue({
        code: 'custom',
        path: ['end_date'],
        message: 'End date cannot be earlier than the start date.',
      })
    }
  })

export type EducationFormValues = z.infer<typeof educationSchema>
