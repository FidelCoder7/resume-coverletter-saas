import { z } from 'zod'

import { EMPLOYMENT_TYPES } from '@/types/resume'

export const experienceSchema = z
  .object({
    company: z
      .string()
      .trim()
      .min(1, 'Company is required.')
      .max(255, 'Company must be less than 255 characters.'),

    job_title: z
      .string()
      .trim()
      .min(1, 'Job title is required.')
      .max(255, 'Job title must be less than 255 characters.'),

    location: z
      .string()
      .trim()
      .max(255, 'Location must be less than 255 characters.')
      .optional()
      .or(z.literal('')),

    employment_type: z.enum(EMPLOYMENT_TYPES, {
      error: 'Employment type is required.',
    }),

    start_date: z.string().min(1, 'Start date is required.'),

    end_date: z.string().optional().or(z.literal('')),

    is_current: z.boolean(),

    description: z
      .string()
      .trim()
      .max(5000, 'Description must be less than 5000 characters.')
      .optional()
      .or(z.literal('')),

    display_order: z.number().int().min(0),
  })
  .superRefine((data, context) => {
    if (!data.is_current && !data.end_date) {
      context.addIssue({
        code: 'custom',
        path: ['end_date'],
        message: 'End date is required when this is not your current position.',
      })
    }

    if (data.is_current && data.end_date) {
      context.addIssue({
        code: 'custom',
        path: ['end_date'],
        message: 'End date must be empty for your current position.',
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

export type ExperienceFormValues = z.infer<typeof experienceSchema>
