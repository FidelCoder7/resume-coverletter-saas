import { useQuery } from '@tanstack/react-query'

import { adminApi } from '@/features/admin/api/admin_api'

export const ADMIN_METRICS_QUERY_KEY = ['admin', 'metrics'] as const

export const ADMIN_METRICS_TIMESERIES_QUERY_KEY = [
  'admin',
  'metrics',
  'timeseries',
] as const

export function useAdminMetrics() {
  return useQuery({
    queryKey: ADMIN_METRICS_QUERY_KEY,
    queryFn: adminApi.getMetrics,
    staleTime: 60 * 1000,
  })
}

export function useAdminMetricsTimeSeries(days = 30) {
  return useQuery({
    queryKey: [...ADMIN_METRICS_TIMESERIES_QUERY_KEY, days],
    queryFn: () => adminApi.getMetricsTimeSeries({ days }),
    staleTime: 60 * 1000,
  })
}
