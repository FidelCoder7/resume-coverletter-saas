import { z } from 'zod'

import { SKILL_LEVELS } from '@/types/resume'

export const skillSchema = z.object({
  name: z
    .string()
    .trim()
    .min(1, 'Skill name is required.')
    .max(100, 'Skill name must be less than 100 characters.'),

  proficiency: z.enum(SKILL_LEVELS),

  display_order: z.number().int().min(0, 'Display order cannot be negative.'),
})

export type SkillFormValues = z.infer<typeof skillSchema>
