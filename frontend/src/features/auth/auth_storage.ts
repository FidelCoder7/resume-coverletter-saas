import type { AccessTokenResponse, TokenResponse } from '@/features/auth/types'

const ACCESS_TOKEN_KEY = 'auth_access_token'
const REFRESH_TOKEN_KEY = 'auth_refresh_token'

function getAccessToken(): string | null {
  return localStorage.getItem(ACCESS_TOKEN_KEY)
}

function getRefreshToken(): string | null {
  return localStorage.getItem(REFRESH_TOKEN_KEY)
}

function setTokens(tokens: TokenResponse | AccessTokenResponse): void {
  localStorage.setItem(ACCESS_TOKEN_KEY, tokens.access_token)

  localStorage.setItem(REFRESH_TOKEN_KEY, tokens.refresh_token)
}

function clearTokens(): void {
  localStorage.removeItem(ACCESS_TOKEN_KEY)
  localStorage.removeItem(REFRESH_TOKEN_KEY)
}

export const authStorage = {
  getAccessToken,
  getRefreshToken,
  setTokens,
  clearTokens,
} as const
