import { Menu } from 'lucide-react'
import { useMatches } from 'react-router-dom'

import { Button } from '@/components/ui/button'
import NotificationMenu from '@/components/navigation/NotificationMenu'
import ThemeToggle from '@/components/navigation/ThemeToggle'
import UserMenu from '@/components/navigation/UserMenu'

interface AdminHeaderProps {
  onMenuClick?: () => void
}

interface RouteHandle {
  title?: string
}

function AdminHeader({ onMenuClick }: AdminHeaderProps) {
  const matches = useMatches()

  const currentMatch = [...matches].reverse().find((match) => {
    const handle = match.handle as RouteHandle | undefined

    return Boolean(handle?.title)
  })

  const handle = currentMatch?.handle as RouteHandle | undefined
  const pageTitle = handle?.title ?? 'Admin Dashboard'

  return (
    <header className="flex h-16 shrink-0 items-center justify-between border-b bg-background px-4 sm:px-6">
      <div className="flex min-w-0 items-center gap-3">
        <Button
          type="button"
          variant="ghost"
          size="icon"
          className="lg:hidden"
          aria-label="Open administrator navigation menu"
          aria-controls="mobile-admin-navigation"
          onClick={onMenuClick}
        >
          <Menu />
        </Button>

        <div className="min-w-0">
          <p className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
            Administration
          </p>
          <h1 className="truncate text-base font-semibold">{pageTitle}</h1>
        </div>
      </div>

      <div className="flex items-center gap-1">
        <NotificationMenu />
        <ThemeToggle />
        <UserMenu />
      </div>
    </header>
  )
}

export default AdminHeader
