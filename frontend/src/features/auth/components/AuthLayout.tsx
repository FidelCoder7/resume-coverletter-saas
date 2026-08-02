import type { ReactNode } from 'react'
import { Link } from 'react-router-dom'

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { appConfig } from '@/app/config'

interface AuthLayoutProps {
  title: string
  description: string
  children: ReactNode
  footer?: ReactNode
}

function AuthLayout({ title, description, children, footer }: AuthLayoutProps) {
  return (
    <main className="flex min-h-screen items-center justify-center bg-background px-4 py-12">
      <div className="w-full max-w-md">
        <div className="mb-8 text-center">
          <Link
            to="/"
            className="inline-block text-2xl font-bold tracking-tight transition-opacity hover:opacity-80"
          >
            {appConfig.appName}
          </Link>
        </div>

        <Card>
          <CardHeader className="px-6 pt-6">
            <CardTitle className="text-2xl">{title}</CardTitle>

            <CardDescription>{description}</CardDescription>
          </CardHeader>

          <CardContent className="px-6 pb-6">{children}</CardContent>
        </Card>

        {footer && (
          <div className="mt-6 text-center text-sm text-muted-foreground">
            {footer}
          </div>
        )}
      </div>
    </main>
  )
}

export default AuthLayout
