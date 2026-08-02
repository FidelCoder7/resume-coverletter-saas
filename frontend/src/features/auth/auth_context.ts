import { createContext } from 'react'

import type { LoginRequest, RegisterRequest, User } from '@/features/auth/types'

export interface AuthContextValue {
  user: User | null
  isAuthenticated: boolean
  isInitializing: boolean
  login: (payload: LoginRequest) => Promise<User>
  register: (payload: RegisterRequest) => Promise<User>
  logout: () => Promise<void>
  refreshSession: () => Promise<User | null>
}

export const AuthContext = createContext<AuthContextValue | undefined>(
  undefined,
)
