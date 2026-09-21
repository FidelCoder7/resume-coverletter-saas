import { useQuery } from '@tanstack/react-query'

import { adminApi } from '@/features/admin/api/admin_api'
import type { AdminAuditLogListParams } from '@/features/admin/types'

export const ADMIN_AUDIT_LOGS_QUERY_KEY = ['admin', 'audit-logs'] as const

export const ADMIN_AUDIT_LOG_QUERY_KEY = ['admin', 'audit-log'] as const

export function useAdminAuditLogs(params?: AdminAuditLogListParams) {
  return useQuery({
    queryKey: [...ADMIN_AUDIT_LOGS_QUERY_KEY, params],
    queryFn: () => adminApi.listAuditLogs(params),
    staleTime: 30 * 1000,
  })
}

export function useAdminAuditLog(auditLogId: string) {
  return useQuery({
    queryKey: [...ADMIN_AUDIT_LOG_QUERY_KEY, auditLogId],
    queryFn: () => adminApi.getAuditLog(auditLogId),
    enabled: Boolean(auditLogId),
    staleTime: 30 * 1000,
  })
}

export function useAdminUserAuditLogs(
  userId: string,
  params?: AdminAuditLogListParams,
) {
  return useQuery({
    queryKey: [...ADMIN_AUDIT_LOGS_QUERY_KEY, 'user', userId, params],
    queryFn: () => adminApi.listUserAuditLogs(userId, params),
    enabled: Boolean(userId),
    staleTime: 30 * 1000,
  })
}

export function useAdminAdminAuditLogs(
  adminId: string,
  params?: AdminAuditLogListParams,
) {
  return useQuery({
    queryKey: [...ADMIN_AUDIT_LOGS_QUERY_KEY, 'admin', adminId, params],
    queryFn: () => adminApi.listAdminAuditLogs(adminId, params),
    enabled: Boolean(adminId),
    staleTime: 30 * 1000,
  })
}
