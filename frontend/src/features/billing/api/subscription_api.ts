import apiClient from '@/api/axios'
import { API_ENDPOINTS } from '@/api/endpoint'

import type {
  PlanLimitListResponse,
  SubscriptionUsage,
} from '@/features/billing/types'

export async function getSubscriptionLimits(): Promise<PlanLimitListResponse> {
  const response = await apiClient.get<PlanLimitListResponse>(
    API_ENDPOINTS.SUBSCRIPTIONS.LIMITS,
  )

  return response.data
}

export async function getSubscriptionUsage(): Promise<SubscriptionUsage> {
  const response = await apiClient.get<SubscriptionUsage>(
    API_ENDPOINTS.SUBSCRIPTIONS.USAGE,
  )

  return response.data
}
