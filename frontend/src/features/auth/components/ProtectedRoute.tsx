import type { ReactNode } from 'react'
import { Navigate, useLocation } from 'react-router-dom'

import { useAuth } from '@/features/auth/hooks/use_auth'

interface ProtectedRouteProps {
  children: ReactNode
}

function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { isAuthenticated, isInitializing } = useAuth()
  const location = useLocation()

  if (isInitializing) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-background px-4">
        <div className="text-center">
          <p className="text-sm text-muted-foreground">
            Checking your session...
          </p>
        </div>
      </main>
    )
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace state={{ from: location }} />
  }

  return <>{children}</>
}

export default ProtectedRoute
