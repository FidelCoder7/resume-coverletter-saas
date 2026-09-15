export interface ATSOptimizationRequest {
  job_description: string
  target_job_title?: string | null
}

export interface ATSOptimizationResponse {
  resume_id: string
  optimized_resume: string
  ats_score: number
  matched_keywords: string[]
  missing_keywords: string[]
  recommendations: string[]
}
