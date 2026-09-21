import apiClient from '@/api/axios'
import { API_ENDPOINTS } from '@/api/endpoint'

import type {
  AdminAccessResponse,
  AdminDashboardMetricsResponse,
  AdminDashboardTimeSeriesParams,
  AdminDashboardTimeSeriesResponse,
  AdminUserActionRequest,
  AdminUserDetail,
  AdminUserListParams,
  AdminUserListResponse,
  AdminAuditLog,
  AdminAuditLogListParams,
  AdminAuditLogListResponse,
} from '@/features/admin/types'

export const adminApi = {
  verifyAccess: async (): Promise<AdminAccessResponse> => {
    const response = await apiClient.get<AdminAccessResponse>(
      API_ENDPOINTS.ADMIN.ACCESS,
    )

    return response.data
  },

  listUsers: async (
    params?: AdminUserListParams,
  ): Promise<AdminUserListResponse> => {
    const response = await apiClient.get<AdminUserListResponse>(
      API_ENDPOINTS.ADMIN.USERS,
      {
        params,
      },
    )

    return response.data
  },

  getUser: async (userId: string): Promise<AdminUserDetail> => {
    const response = await apiClient.get<AdminUserDetail>(
      API_ENDPOINTS.ADMIN.USER_BY_ID(userId),
    )

    return response.data
  },

  suspendUser: async (
    userId: string,
    payload?: AdminUserActionRequest,
  ): Promise<AdminUserDetail> => {
    const response = await apiClient.post<AdminUserDetail>(
      API_ENDPOINTS.ADMIN.SUSPEND_USER(userId),
      payload,
    )

    return response.data
  },

  reactivateUser: async (
    userId: string,
    payload?: AdminUserActionRequest,
  ): Promise<AdminUserDetail> => {
    const response = await apiClient.post<AdminUserDetail>(
      API_ENDPOINTS.ADMIN.REACTIVATE_USER(userId),
      payload,
    )

    return response.data
  },

  getMetrics: async (): Promise<AdminDashboardMetricsResponse> => {
    const response = await apiClient.get<AdminDashboardMetricsResponse>(
      API_ENDPOINTS.ADMIN.METRICS,
    )

    return response.data
  },

  getMetricsTimeSeries: async (
    params?: AdminDashboardTimeSeriesParams,
  ): Promise<AdminDashboardTimeSeriesResponse> => {
    const response = await apiClient.get<AdminDashboardTimeSeriesResponse>(
      API_ENDPOINTS.ADMIN.METRICS_TIMESERIES,
      {
        params,
      },
    )

    return response.data
  },

  listAuditLogs: async (
    params?: AdminAuditLogListParams,
  ): Promise<AdminAuditLogListResponse> => {
    const response = await apiClient.get<AdminAuditLogListResponse>(
      API_ENDPOINTS.ADMIN.AUDIT_LOGS,
      {
        params,
      },
    )

    return response.data
  },

  getAuditLog: async (auditLogId: string): Promise<AdminAuditLog> => {
    const response = await apiClient.get<AdminAuditLog>(
      API_ENDPOINTS.ADMIN.AUDIT_LOG_BY_ID(auditLogId),
    )

    return response.data
  },

  listUserAuditLogs: async (
    userId: string,
    params?: AdminAuditLogListParams,
  ): Promise<AdminAuditLogListResponse> => {
    const response = await apiClient.get<AdminAuditLogListResponse>(
      API_ENDPOINTS.ADMIN.USER_AUDIT_LOGS(userId),
      {
        params,
      },
    )

    return response.data
  },

  listAdminAuditLogs: async (
    adminId: string,
    params?: AdminAuditLogListParams,
  ): Promise<AdminAuditLogListResponse> => {
    const response = await apiClient.get<AdminAuditLogListResponse>(
      API_ENDPOINTS.ADMIN.ADMIN_AUDIT_LOGS(adminId),
      {
        params,
      },
    )

    return response.data
  },
}
