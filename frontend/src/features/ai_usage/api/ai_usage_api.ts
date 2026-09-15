import apiClient from '@/api/axios'
import { API_ENDPOINTS } from '@/api/endpoint'

import type {
  AIFeatureUsage,
  AIUsage,
  AIUsageDashboard,
  AIUsageListResponse,
  AIUsageSummary,
} from '@/features/ai_usage/types'

interface AIUsagePeriod {
  start_date: string
  end_date: string
}

export async function listAIUsage(): Promise<AIUsage[]> {
  const response = await apiClient.get<AIUsageListResponse>(
    API_ENDPOINTS.AI_USAGE.BASE,
  )

  return response.data.items
}

export async function getAIUsage(usageId: string): Promise<AIUsage> {
  const response = await apiClient.get<AIUsage>(
    API_ENDPOINTS.AI_USAGE.BY_ID(usageId),
  )

  return response.data
}

export async function listResumeAIUsage(resumeId: string): Promise<AIUsage[]> {
  const response = await apiClient.get<AIUsageListResponse>(
    API_ENDPOINTS.AI_USAGE.BY_RESUME(resumeId),
  )

  return response.data.items
}

export async function listCoverLetterAIUsage(
  coverLetterId: string,
): Promise<AIUsage[]> {
  const response = await apiClient.get<AIUsageListResponse>(
    API_ENDPOINTS.AI_USAGE.BY_COVER_LETTER(coverLetterId),
  )

  return response.data.items
}

export async function getAIUsageSummary(
  period: AIUsagePeriod,
): Promise<AIUsageSummary> {
  const response = await apiClient.get<AIUsageSummary>(
    API_ENDPOINTS.AI_USAGE.SUMMARY,
    {
      params: period,
    },
  )

  return response.data
}

export async function getAIFeatureBreakdown(
  period: AIUsagePeriod,
): Promise<AIFeatureUsage[]> {
  const response = await apiClient.get<AIFeatureUsage[]>(
    API_ENDPOINTS.AI_USAGE.FEATURES,
    {
      params: period,
    },
  )

  return response.data
}

export async function getAIUsageDashboard(
  period: AIUsagePeriod,
): Promise<AIUsageDashboard> {
  const response = await apiClient.get<AIUsageDashboard>(
    API_ENDPOINTS.AI_USAGE.DASHBOARD,
    {
      params: period,
    },
  )

  return response.data
}
