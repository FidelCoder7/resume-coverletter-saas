export const AI_FEATURES = [
  'cover_letter_generation',
  'cover_letter_regeneration',
  'resume_generation',
  'ats_optimization',
] as const

export type AIFeature = (typeof AI_FEATURES)[number]

export const AI_REQUEST_STATUSES = ['success', 'failed', 'cancelled'] as const

export type AIRequestStatus = (typeof AI_REQUEST_STATUSES)[number]

export interface AIUsage {
  id: string
  user_id: string
  resume_id: string | null
  cover_letter_id: string | null
  feature: AIFeature
  provider: string
  model: string
  prompt_version: string
  prompt_tokens: number | null
  completion_tokens: number | null
  total_tokens: number | null
  estimated_cost: number | null
  latency_ms: number | null
  status: AIRequestStatus
  error_message: string | null
  created_at: string
}

export interface AIUsageListResponse {
  items: AIUsage[]
}

export interface AIUsageSummary {
  total_requests: number
  successful_requests: number
  failed_requests: number
  total_tokens: number
  estimated_cost: number
  average_latency_ms: number | null
}

export interface AIFeatureUsage {
  feature: AIFeature
  requests: number
  total_tokens: number
}

export interface AIUsageDashboard {
  summary: AIUsageSummary
  features: AIFeatureUsage[]
}
