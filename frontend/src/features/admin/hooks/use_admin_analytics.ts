import { useQuery } from '@tanstack/react-query'

import { adminApi } from '@/features/admin/api/admin_api'

export const ADMIN_SUBSCRIPTION_ANALYTICS_QUERY_KEY = [
  'admin',
  'analytics',
  'subscriptions',
] as const

export const ADMIN_PAYMENT_ANALYTICS_QUERY_KEY = [
  'admin',
  'analytics',
  'payments',
] as const

export const ADMIN_AI_ANALYTICS_QUERY_KEY = [
  'admin',
  'analytics',
  'ai',
] as const

export function useAdminSubscriptionAnalytics() {
  return useQuery({
    queryKey: ADMIN_SUBSCRIPTION_ANALYTICS_QUERY_KEY,
    queryFn: adminApi.getSubscriptionAnalytics,
    staleTime: 60 * 1000,
  })
}

export function useAdminPaymentAnalytics(days = 30) {
  return useQuery({
    queryKey: [...ADMIN_PAYMENT_ANALYTICS_QUERY_KEY, days],
    queryFn: () => adminApi.getPaymentAnalytics({ days }),
    staleTime: 60 * 1000,
  })
}

export function useAdminAIAnalytics(days = 30) {
  return useQuery({
    queryKey: [...ADMIN_AI_ANALYTICS_QUERY_KEY, days],
    queryFn: () => adminApi.getAIAnalytics({ days }),
    staleTime: 60 * 1000,
  })
}
