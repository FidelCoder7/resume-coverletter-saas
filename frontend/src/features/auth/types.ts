import type { AccountStatus, SubscriptionPlan, UserRole } from '@/types/user'

export interface User {
  id: string
  email: string
  full_name: string
  is_email_verified: boolean
  role: UserRole
  subscription_plan: SubscriptionPlan
  status: AccountStatus
}

export interface RegisterRequest {
  email: string
  full_name: string
  password: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
  user: User
}

export interface RefreshTokenRequest {
  refresh_token: string
}

export interface AccessTokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
}

export interface VerifyEmailRequest {
  token: string
}

export interface ForgotPasswordRequest {
  email: string
}

export interface ResetPasswordRequest {
  token: string
  new_password: string
}
