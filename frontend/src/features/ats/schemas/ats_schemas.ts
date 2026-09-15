import { z } from 'zod'

export const atsOptimizationSchema = z.object({
  job_description: z
    .string()
    .trim()
    .min(1, 'Job description is required.')
    .max(10000, 'Job description must be 10,000 characters or fewer.'),

  target_job_title: z
    .string()
    .trim()
    .max(255, 'Target job title must be 255 characters or fewer.')
    .optional()
    .or(z.literal('')),
})

export type ATSOptimizationFormValues = z.infer<typeof atsOptimizationSchema>
