export interface CoverLetterGenerationRequest {
  title: string
  company_name: string
  job_title: string
  job_description: string
}

export interface CoverLetterRegenerationRequest {
  job_description: string
}

export interface CoverLetter {
  id: string
  resume_id: string
  title: string
  company_name: string
  job_title: string
  content: string
  created_at: string
  updated_at: string
}

export interface CoverLetterListResponse {
  cover_letters: CoverLetter[]
}
