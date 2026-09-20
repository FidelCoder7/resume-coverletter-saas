import type { ReactNode } from 'react'
import { Navigate, useLocation } from 'react-router-dom'

import { useAdminAccess } from '@/features/admin/hooks/use_admin_access'
import { useAuth } from '@/features/auth/hooks/use_auth'

interface AdminRouteProps {
  children: ReactNode
}

function AdminRoute({ children }: AdminRouteProps) {
  const { isAuthenticated, isInitializing, user } = useAuth()
  const location = useLocation()

  const shouldVerifyAccess =
    isAuthenticated && !isInitializing && user?.role === 'admin'

  const { isLoading: isCheckingAdminAccess, isError: isAdminAccessDenied } =
    useAdminAccess(shouldVerifyAccess)

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

  if (user?.role !== 'admin') {
    return <Navigate to="/dashboard" replace />
  }

  if (isCheckingAdminAccess) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-background px-4">
        <div className="text-center">
          <p className="text-sm text-muted-foreground">
            Verifying administrator access...
          </p>
        </div>
      </main>
    )
  }

  if (isAdminAccessDenied) {
    return <Navigate to="/dashboard" replace />
  }

  return <>{children}</>
}

export default AdminRoute
