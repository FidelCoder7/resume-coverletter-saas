import { z } from 'zod'

export const resumeGenerationSchema = z.object({
  target_job_title: z
    .string()
    .trim()
    .max(255, 'Target job title must be 255 characters or fewer.')
    .optional()
    .or(z.literal('')),

  job_description: z
    .string()
    .trim()
    .min(20, 'Job description must be at least 20 characters.')
    .max(10000, 'Job description must be 10,000 characters or fewer.')
    .optional()
    .or(z.literal('')),
})

export type ResumeGenerationFormValues = z.infer<typeof resumeGenerationSchema>
