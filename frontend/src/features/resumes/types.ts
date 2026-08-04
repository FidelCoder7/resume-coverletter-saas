import type { EmploymentType, SkillLevel } from '@/types/resume'

export interface Resume {
  id: string
  user_id: string

  title: string
  summary: string | null

  generated_content: string | null
  generated_at: string | null

  is_default: boolean

  created_at: string
  updated_at: string
}

export interface CreateResumeRequest {
  title: string
  summary?: string | null
}

export interface UpdateResumeRequest {
  title: string
  summary?: string | null
}

export interface ResumeListResponse {
  resumes: Resume[]
}

export interface ResumeGenerationRequest {
  target_job_title?: string | null
  job_description?: string | null
}

export interface Experience {
  id: string
  resume_id: string

  company: string
  job_title: string
  location: string | null

  employment_type: EmploymentType

  start_date: string
  end_date: string | null

  is_current: boolean

  description: string | null

  display_order: number

  created_at: string
  updated_at: string
}

export interface CreateExperienceRequest {
  company: string
  job_title: string
  location?: string | null
  employment_type: EmploymentType
  start_date: string
  end_date?: string | null
  is_current: boolean
  description?: string | null
  display_order: number
}

export type UpdateExperienceRequest = CreateExperienceRequest

export interface ExperienceListResponse {
  experiences: Experience[]
}

export interface Education {
  id: string
  resume_id: string

  institution: string
  degree: string
  field_of_study: string
  location: string | null
  grade: string | null

  start_date: string
  end_date: string | null

  is_current: boolean

  description: string | null

  display_order: number

  created_at: string
  updated_at: string
}

export interface CreateEducationRequest {
  institution: string
  degree: string
  field_of_study: string
  location?: string | null
  grade?: string | null
  start_date: string
  end_date?: string | null
  is_current: boolean
  description?: string | null
  display_order: number
}

export type UpdateEducationRequest = CreateEducationRequest

export type EducationListResponse = Education[]

export interface Skill {
  id: string
  resume_id: string

  name: string
  proficiency: SkillLevel

  display_order: number

  created_at: string
  updated_at: string
}

export interface CreateSkillRequest {
  name: string
  proficiency: SkillLevel
  display_order: number
}

export type UpdateSkillRequest = CreateSkillRequest

export interface SkillListResponse {
  skills: Skill[]
}

export interface Project {
  id: string
  resume_id: string

  name: string
  description: string
  technologies: string

  project_url: string | null
  repository_url: string | null

  start_date: string | null
  end_date: string | null

  is_ongoing: boolean

  display_order: number

  created_at: string
  updated_at: string
}

export interface CreateProjectRequest {
  name: string
  description: string
  technologies: string
  project_url?: string | null
  repository_url?: string | null
  start_date?: string | null
  end_date?: string | null
  is_ongoing: boolean
  display_order: number
}

export type UpdateProjectRequest = CreateProjectRequest

export interface ProjectListResponse {
  projects: Project[]
}

export interface Certification {
  id: string
  resume_id: string

  name: string
  issuing_organization: string

  credential_id: string | null
  credential_url: string | null

  issue_date: string
  expiration_date: string | null

  does_not_expire: boolean

  display_order: number

  created_at: string
  updated_at: string
}

export interface CreateCertificationRequest {
  name: string
  issuing_organization: string
  credential_id?: string | null
  credential_url?: string | null
  issue_date: string
  expiration_date?: string | null
  does_not_expire: boolean
  display_order: number
}

export type UpdateCertificationRequest = CreateCertificationRequest

export interface CertificationListResponse {
  certifications: Certification[]
}
