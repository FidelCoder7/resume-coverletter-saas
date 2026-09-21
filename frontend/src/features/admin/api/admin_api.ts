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
}
