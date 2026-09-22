import { useQuery } from '@tanstack/react-query'

import { adminApi } from '@/features/admin/api/admin_api'

export const ADMIN_ACCESS_QUERY_KEY = ['admin', 'access'] as const

export function useAdminAccess(enabled = true) {
  return useQuery({
    queryKey: ADMIN_ACCESS_QUERY_KEY,
    queryFn: adminApi.verifyAccess,
    enabled,
    staleTime: 5 * 60 * 1000,
    retry: false,
  })
}
