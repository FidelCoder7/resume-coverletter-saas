import {
  useCallback,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from 'react'

import {
  getCurrentUser,
  login as loginApi,
  logout as logoutApi,
  register as registerApi,
  refreshToken as refreshTokenApi,
} from '@/features/auth/api/auth_api'
import { authStorage } from '@/features/auth/auth_storage'
import { AuthContext } from '@/features/auth/auth_context'
import type { LoginRequest, RegisterRequest, User } from '@/features/auth/types'

interface AuthProviderProps {
  children: ReactNode
}

function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null)
  const [isInitializing, setIsInitializing] = useState(true)

  const isAuthenticated = user !== null

  const refreshSession = useCallback(async (): Promise<User | null> => {
    const refreshToken = authStorage.getRefreshToken()

    if (!refreshToken) {
      setUser(null)
      return null
    }

    try {
      const tokens = await refreshTokenApi({
        refresh_token: refreshToken,
      })

      authStorage.setTokens(tokens)

      const currentUser = await getCurrentUser()

      setUser(currentUser)

      return currentUser
    } catch {
      authStorage.clearTokens()
      setUser(null)

      return null
    }
  }, [])

  useEffect(() => {
    let isMounted = true

    const initializeAuth = async (): Promise<void> => {
      const accessToken = authStorage.getAccessToken()
      const refreshToken = authStorage.getRefreshToken()

      if (!accessToken && !refreshToken) {
        if (isMounted) {
          setIsInitializing(false)
        }

        return
      }

      try {
        const currentUser = await getCurrentUser()

        if (isMounted) {
          setUser(currentUser)
        }
      } catch {
        await refreshSession()
      } finally {
        if (isMounted) {
          setIsInitializing(false)
        }
      }
    }

    void initializeAuth()

    return () => {
      isMounted = false
    }
  }, [refreshSession])

  const login = useCallback(async (payload: LoginRequest): Promise<User> => {
    const response = await loginApi(payload)

    authStorage.setTokens(response)

    setUser(response.user)

    return response.user
  }, [])

  const register = useCallback(
    async (payload: RegisterRequest): Promise<User> => {
      const newUser = await registerApi(payload)

      return newUser
    },
    [],
  )

  const logout = useCallback(async (): Promise<void> => {
    const refreshToken = authStorage.getRefreshToken()

    try {
      if (refreshToken) {
        await logoutApi(refreshToken)
      }
    } finally {
      authStorage.clearTokens()
      setUser(null)
    }
  }, [])

  const value = useMemo(
    () => ({
      user,
      isAuthenticated,
      isInitializing,
      login,
      register,
      logout,
      refreshSession,
    }),
    [
      user,
      isAuthenticated,
      isInitializing,
      login,
      register,
      logout,
      refreshSession,
    ],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export default AuthProvider
