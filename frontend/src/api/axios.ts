import axios, { type AxiosError, type InternalAxiosRequestConfig } from 'axios'

import { appConfig } from '@/app/config'
import { API_ENDPOINTS } from '@/api/endpoint'
import { authStorage } from '@/features/auth/auth_storage'
import type { AccessTokenResponse } from '@/features/auth/types'

interface RetryableRequestConfig extends InternalAxiosRequestConfig {
  _retry?: boolean
}

const apiClient = axios.create({
  baseURL: appConfig.apiBaseUrl,
  timeout: 15_000,
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },
})

const refreshClient = axios.create({
  baseURL: appConfig.apiBaseUrl,
  timeout: 15_000,
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },
})

let refreshPromise: Promise<AccessTokenResponse> | null = null

function isAuthEndpoint(url?: string): boolean {
  if (!url) {
    return false
  }

  return (
    url === API_ENDPOINTS.AUTH.LOGIN ||
    url === API_ENDPOINTS.AUTH.REFRESH ||
    url === API_ENDPOINTS.AUTH.LOGOUT ||
    url === API_ENDPOINTS.AUTH.REGISTER
  )
}

async function refreshAccessToken(): Promise<AccessTokenResponse> {
  const refreshToken = authStorage.getRefreshToken()

  if (!refreshToken) {
    throw new Error('No refresh token available.')
  }

  if (!refreshPromise) {
    refreshPromise = refreshClient
      .post<AccessTokenResponse>(API_ENDPOINTS.AUTH.REFRESH, {
        refresh_token: refreshToken,
      })
      .then((response) => {
        authStorage.setTokens(response.data)

        return response.data
      })
      .finally(() => {
        refreshPromise = null
      })
  }

  return refreshPromise
}

apiClient.interceptors.request.use((config) => {
  const accessToken = authStorage.getAccessToken()

  if (accessToken && !isAuthEndpoint(config.url)) {
    config.headers.Authorization = `Bearer ${accessToken}`
  }

  return config
})

apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as RetryableRequestConfig | undefined

    if (
      error.response?.status !== 401 ||
      !originalRequest ||
      originalRequest._retry ||
      isAuthEndpoint(originalRequest.url)
    ) {
      return Promise.reject(error)
    }

    originalRequest._retry = true

    try {
      const tokens = await refreshAccessToken()

      originalRequest.headers.Authorization = `Bearer ${tokens.access_token}`

      return apiClient(originalRequest)
    } catch (refreshError) {
      authStorage.clearTokens()

      return Promise.reject(refreshError)
    }
  },
)

export default apiClient
