import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import { adminApi } from '@/features/admin/api/admin_api'
import type {
  AdminUserActionRequest,
  AdminUserListParams,
} from '@/features/admin/types'

export const ADMIN_USERS_QUERY_KEY = ['admin', 'users'] as const

export const ADMIN_USER_QUERY_KEY = ['admin', 'user'] as const

export function useAdminUsers(params?: AdminUserListParams) {
  return useQuery({
    queryKey: [...ADMIN_USERS_QUERY_KEY, params],
    queryFn: () => adminApi.listUsers(params),
    staleTime: 30 * 1000,
  })
}

export function useAdminUser(userId: string) {
  return useQuery({
    queryKey: [...ADMIN_USER_QUERY_KEY, userId],
    queryFn: () => adminApi.getUser(userId),
    enabled: Boolean(userId),
    staleTime: 30 * 1000,
  })
}

export function useSuspendAdminUser() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({
      userId,
      payload,
    }: {
      userId: string
      payload?: AdminUserActionRequest
    }) => adminApi.suspendUser(userId, payload),
    onSuccess: async (user) => {
      await Promise.all([
        queryClient.invalidateQueries({
          queryKey: ADMIN_USERS_QUERY_KEY,
        }),
        queryClient.invalidateQueries({
          queryKey: [...ADMIN_USER_QUERY_KEY, user.id],
        }),
        queryClient.invalidateQueries({
          queryKey: ['admin', 'metrics'],
        }),
      ])
    },
  })
}

export function useReactivateAdminUser() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({
      userId,
      payload,
    }: {
      userId: string
      payload?: AdminUserActionRequest
    }) => adminApi.reactivateUser(userId, payload),
    onSuccess: async (user) => {
      await Promise.all([
        queryClient.invalidateQueries({
          queryKey: ADMIN_USERS_QUERY_KEY,
        }),
        queryClient.invalidateQueries({
          queryKey: [...ADMIN_USER_QUERY_KEY, user.id],
        }),
        queryClient.invalidateQueries({
          queryKey: ['admin', 'metrics'],
        }),
      ])
    },
  })
}
