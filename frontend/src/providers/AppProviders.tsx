import type { ReactNode } from 'react'

import AuthProvider from '@/features/auth/auth_provider'
import QueryProvider from './QueryProvider'
import ThemeProvider from './ThemeProvider'

interface AppProvidersProps {
  children: ReactNode
}

function AppProviders({ children }: AppProvidersProps) {
  return (
    <QueryProvider>
      {' '}
      <ThemeProvider>
        {' '}
        <AuthProvider>{children}</AuthProvider>{' '}
      </ThemeProvider>{' '}
    </QueryProvider>
  )
}

export default AppProviders
