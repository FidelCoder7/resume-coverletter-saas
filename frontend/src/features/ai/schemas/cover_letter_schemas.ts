import { z } from 'zod'

export const coverLetterGenerationSchema = z.object({
  title: z
    .string()
    .trim()
    .min(1, 'Title is required.')
    .max(255, 'Title must be 255 characters or fewer.'),

  company_name: z
    .string()
    .trim()
    .min(1, 'Company name is required.')
    .max(255, 'Company name must be 255 characters or fewer.'),

  job_title: z
    .string()
    .trim()
    .min(1, 'Job title is required.')
    .max(255, 'Job title must be 255 characters or fewer.'),

  job_description: z
    .string()
    .trim()
    .min(20, 'Job description must be at least 20 characters.'),
})

export const coverLetterRegenerationSchema = z.object({
  job_description: z
    .string()
    .trim()
    .min(20, 'Job description must be at least 20 characters.'),
})

export type CoverLetterGenerationFormValues = z.infer<
  typeof coverLetterGenerationSchema
>

export type CoverLetterRegenerationFormValues = z.infer<
  typeof coverLetterRegenerationSchema
>
