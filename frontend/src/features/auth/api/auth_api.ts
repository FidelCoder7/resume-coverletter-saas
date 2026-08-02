import apiClient from '@/api/axios'
import { API_ENDPOINTS } from '@/api/endpoint'
import { appConfig } from '@/app/config'
import type {
  AccessTokenResponse,
  ForgotPasswordRequest,
  LoginRequest,
  RefreshTokenRequest,
  RegisterRequest,
  ResetPasswordRequest,
  TokenResponse,
  User,
  VerifyEmailRequest,
} from '@/features/auth/types'

export async function register(payload: RegisterRequest): Promise<User> {
  const response = await apiClient.post<User>(
    API_ENDPOINTS.AUTH.REGISTER,
    payload,
  )

  return response.data
}

export async function login(payload: LoginRequest): Promise<TokenResponse> {
  const formData = new URLSearchParams()

  formData.append('username', payload.email)
  formData.append('password', payload.password)

  const response = await apiClient.post<TokenResponse>(
    API_ENDPOINTS.AUTH.LOGIN,
    formData,
    {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    },
  )

  return response.data
}

export async function refreshToken(
  payload: RefreshTokenRequest,
): Promise<AccessTokenResponse> {
  const response = await apiClient.post<AccessTokenResponse>(
    API_ENDPOINTS.AUTH.REFRESH,
    payload,
  )

  return response.data
}

export async function logout(refreshTokenValue: string): Promise<void> {
  await apiClient.post(API_ENDPOINTS.AUTH.LOGOUT, {
    refresh_token: refreshTokenValue,
  })
}

export async function getCurrentUser(): Promise<User> {
  const response = await apiClient.get<User>(API_ENDPOINTS.AUTH.ME)

  return response.data
}

export async function verifyEmail(payload: VerifyEmailRequest): Promise<void> {
  await apiClient.post(API_ENDPOINTS.AUTH.VERIFY_EMAIL, payload)
}

export async function forgotPassword(
  payload: ForgotPasswordRequest,
): Promise<void> {
  await apiClient.post(API_ENDPOINTS.AUTH.FORGOT_PASSWORD, payload)
}

export async function resetPassword(
  payload: ResetPasswordRequest,
): Promise<void> {
  await apiClient.post(API_ENDPOINTS.AUTH.RESET_PASSWORD, payload)
}

export function getGoogleLoginUrl(): string {
  return `${appConfig.apiBaseUrl}${API_ENDPOINTS.AUTH.GOOGLE_LOGIN}`
}
