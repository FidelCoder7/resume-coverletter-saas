import type { ReactNode } from 'react'
import QueryProvider from './QueryProvider'
import ThemeProvider from './ThemeProvider'

interface AppProvidersProps {
  children: ReactNode
}

function AppProviders({ children }: AppProvidersProps) {
  return (
    <QueryProvider>
      {' '}
      <ThemeProvider>{children}</ThemeProvider>{' '}
    </QueryProvider>
  )
}

export default AppProviders
