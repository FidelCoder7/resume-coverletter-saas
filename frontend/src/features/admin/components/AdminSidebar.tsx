import { Activity, LayoutDashboard, ShieldCheck, Users, X } from 'lucide-react'
import { NavLink } from 'react-router-dom'

import { appConfig } from '@/app/config'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'

const navigationItems = [
  {
    label: 'Dashboard',
    to: '/admin',
    icon: LayoutDashboard,
  },
  {
    label: 'Users',
    to: '/admin/users',
    icon: Users,
  },
  {
    label: 'Audit Logs',
    to: '/admin/audit-logs',
    icon: Activity,
  },
] as const

interface AdminSidebarProps {
  isMobileOpen?: boolean
  onMobileClose?: () => void
}

function AdminSidebar({
  isMobileOpen = false,
  onMobileClose,
}: AdminSidebarProps) {
  const handleNavigation = () => {
    onMobileClose?.()
  }

  const navigation = (
    <nav
      aria-label="Administrator navigation"
      className="flex-1 space-y-1 overflow-y-auto p-4"
    >
      {navigationItems.map((item) => {
        const Icon = item.icon

        return (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.to === '/admin'}
            onClick={handleNavigation}
            className={({ isActive }) =>
              cn(
                'flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors',
                'text-muted-foreground hover:bg-muted hover:text-foreground',
                isActive && 'bg-primary/10 text-primary',
              )
            }
          >
            <Icon className="size-4 shrink-0" />
            <span>{item.label}</span>
          </NavLink>
        )
      })}
    </nav>
  )

  return (
    <>
      <aside className="hidden w-64 shrink-0 border-r bg-card lg:flex lg:flex-col">
        <div className="flex h-16 items-center gap-2 border-b px-6">
          <ShieldCheck className="size-5 text-primary" />
          <span className="text-lg font-semibold tracking-tight">
            {appConfig.appName}
          </span>
        </div>

        <div className="border-b px-4 py-3">
          <p className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
            Administration
          </p>
        </div>

        {navigation}
      </aside>

      {isMobileOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/50 lg:hidden"
          aria-hidden="true"
          onClick={onMobileClose}
        />
      )}

      <aside
        id="mobile-admin-navigation"
        aria-label="Mobile administrator navigation"
        className={cn(
          'fixed inset-y-0 left-0 z-50 flex w-72 max-w-[85vw] flex-col border-r bg-card shadow-xl transition-transform duration-200 ease-in-out lg:hidden',
          isMobileOpen ? 'translate-x-0' : '-translate-x-full',
        )}
      >
        <div className="flex h-16 shrink-0 items-center justify-between border-b px-4">
          <div className="flex items-center gap-2 text-lg font-semibold tracking-tight">
            <ShieldCheck className="size-5 text-primary" />
            <span>{appConfig.appName}</span>
          </div>

          <Button
            type="button"
            variant="ghost"
            size="icon"
            aria-label="Close administrator navigation menu"
            onClick={onMobileClose}
          >
            <X />
          </Button>
        </div>

        <div className="border-b px-4 py-3">
          <p className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
            Administration
          </p>
        </div>

        {navigation}
      </aside>
    </>
  )
}

export default AdminSidebar
