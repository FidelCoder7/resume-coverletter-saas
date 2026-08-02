import { useState } from 'react'
import { LogOut, Settings, UserCircle } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

import { Button } from '@/components/ui/button'
import { useAuth } from '@/features/auth/hooks/use_auth'
import { cn } from '@/lib/utils'

function getInitials(fullName: string): string {
  const names = fullName.trim().split(/\s+/)

  if (names.length === 0 || !names[0]) {
    return '?'
  }

  if (names.length === 1) {
    return names[0].charAt(0).toUpperCase()
  }

  return `${names[0].charAt(0)}${names[names.length - 1].charAt(0)}`.toUpperCase()
}

function formatRole(role: string): string {
  return role.charAt(0).toUpperCase() + role.slice(1)
}

function UserMenu() {
  const navigate = useNavigate()
  const { user, logout } = useAuth()
  const [isOpen, setIsOpen] = useState(false)
  const [isLoggingOut, setIsLoggingOut] = useState(false)

  if (!user) {
    return null
  }

  const initials = getInitials(user.full_name)

  const handleLogout = async () => {
    setIsLoggingOut(true)

    try {
      await logout()
      navigate('/login', { replace: true })
    } finally {
      setIsLoggingOut(false)
    }
  }

  const handleNavigation = (path: string) => {
    setIsOpen(false)
    navigate(path)
  }

  return (
    <div className="relative">
      <Button
        type="button"
        variant="ghost"
        className="h-10 gap-2 px-2"
        aria-expanded={isOpen}
        aria-haspopup="menu"
        aria-label="Open user menu"
        onClick={() => {
          setIsOpen((current) => !current)
        }}
      >
        <span className="flex size-8 items-center justify-center rounded-full bg-primary/10 text-sm font-semibold text-primary">
          {initials}
        </span>

        <span className="hidden max-w-32 truncate text-sm font-medium sm:inline">
          {user.full_name}
        </span>
      </Button>

      {isOpen && (
        <>
          <button
            type="button"
            className="fixed inset-0 z-40 cursor-default"
            aria-label="Close user menu"
            onClick={() => {
              setIsOpen(false)
            }}
          />

          <div
            role="menu"
            aria-label="User menu"
            className="absolute right-0 z-50 mt-2 w-64 overflow-hidden rounded-xl border bg-card text-card-foreground shadow-lg"
          >
            <div className="border-b px-4 py-3">
              <div className="flex items-center gap-3">
                <span className="flex size-10 shrink-0 items-center justify-center rounded-full bg-primary/10 font-semibold text-primary">
                  {initials}
                </span>

                <div className="min-w-0">
                  <p className="truncate text-sm font-semibold">
                    {user.full_name}
                  </p>

                  <p className="truncate text-xs text-muted-foreground">
                    {user.email}
                  </p>
                </div>
              </div>

              <div className="mt-3">
                <span className="inline-flex rounded-full bg-muted px-2 py-1 text-xs font-medium text-muted-foreground">
                  {formatRole(user.role)}
                </span>
              </div>
            </div>

            <div className="p-1">
              <button
                type="button"
                role="menuitem"
                className={cn(
                  'flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm',
                  'text-muted-foreground transition-colors',
                  'hover:bg-muted hover:text-foreground',
                )}
                onClick={() => {
                  handleNavigation('/profile')
                }}
              >
                <UserCircle className="size-4" />
                <span>Profile</span>
              </button>

              <button
                type="button"
                role="menuitem"
                className={cn(
                  'flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm',
                  'text-muted-foreground transition-colors',
                  'hover:bg-muted hover:text-foreground',
                )}
                onClick={() => {
                  handleNavigation('/settings')
                }}
              >
                <Settings className="size-4" />
                <span>Settings</span>
              </button>

              <div className="my-1 border-t" />

              <button
                type="button"
                role="menuitem"
                disabled={isLoggingOut}
                className={cn(
                  'flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm',
                  'text-destructive transition-colors',
                  'hover:bg-destructive/10',
                  'disabled:pointer-events-none disabled:opacity-50',
                )}
                onClick={() => {
                  void handleLogout()
                }}
              >
                <LogOut className="size-4" />
                <span>{isLoggingOut ? 'Signing out...' : 'Sign out'}</span>
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  )
}

export default UserMenu
