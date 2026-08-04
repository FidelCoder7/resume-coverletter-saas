import { z } from 'zod'

export const createResumeSchema = z.object({
  title: z
    .string()
    .trim()
    .min(1, 'Resume title is required.')
    .max(255, 'Resume title must be less than 255 characters.'),

  summary: z
    .string()
    .trim()
    .max(5000, 'Summary must be less than 5000 characters.')
    .optional()
    .or(z.literal('')),
})

export type CreateResumeFormValues = z.infer<typeof createResumeSchema>

export const updateResumeSchema = z.object({
  title: z
    .string()
    .trim()
    .min(1, 'Resume title is required.')
    .max(255, 'Resume title must be less than 255 characters.'),

  summary: z
    .string()
    .trim()
    .max(5000, 'Summary must be less than 5000 characters.')
    .optional()
    .or(z.literal('')),
})

export type UpdateResumeFormValues = z.infer<typeof updateResumeSchema>
