export const EMPLOYMENT_TYPES = [
  'full_time',
  'part_time',
  'contract',
  'internship',
  'freelance',
  'volunteer',
  'apprenticeship',
  'temporary',
  'seasonal',
] as const

export type EmploymentType = (typeof EMPLOYMENT_TYPES)[number]

export const SKILL_LEVELS = [
  'beginner',
  'intermediate',
  'advanced',
  'expert',
] as const

export type SkillLevel = (typeof SKILL_LEVELS)[number]
