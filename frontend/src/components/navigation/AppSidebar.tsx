import {
  Bot,
  CreditCard,
  FileText,
  LayoutDashboard,
  Settings,
  Sparkles,
  Target,
  X,
} from 'lucide-react'
import { NavLink } from 'react-router-dom'

import { appConfig } from '@/app/config'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'

const navigationItems = [
  {
    label: 'Dashboard',
    to: '/dashboard',
    icon: LayoutDashboard,
  },
  {
    label: 'Resumes',
    to: '/resumes',
    icon: FileText,
  },
  {
    label: 'Cover Letters',
    to: '/cover-letters',
    icon: FileText,
  },
  {
    label: 'AI Tools',
    to: '/ai',
    icon: Bot,
  },
  {
    label: 'ATS Optimization',
    to: '/ats',
    icon: Target,
  },
  {
    label: 'Billing',
    to: '/billing',
    icon: CreditCard,
  },
  {
    label: 'Settings',
    to: '/settings',
    icon: Settings,
  },
] as const

interface AppSidebarProps {
  isMobileOpen?: boolean
  onMobileClose?: () => void
}

function AppSidebar({ isMobileOpen = false, onMobileClose }: AppSidebarProps) {
  const handleNavigation = () => {
    onMobileClose?.()
  }

  const navigation = (
    <nav
      aria-label="Application navigation"
      className="flex-1 space-y-1 overflow-y-auto p-4"
    >
      {navigationItems.map((item) => {
        const Icon = item.icon

        return (
          <NavLink
            key={item.to}
            to={item.to}
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
        <div className="flex h-16 items-center border-b px-6">
          <NavLink
            to="/dashboard"
            className="flex items-center gap-2 text-lg font-semibold tracking-tight"
          >
            <Sparkles className="size-5 text-primary" />
            <span>{appConfig.appName}</span>
          </NavLink>
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
        id="mobile-navigation"
        aria-label="Mobile application navigation"
        className={cn(
          'fixed inset-y-0 left-0 z-50 flex w-72 max-w-[85vw] flex-col border-r bg-card shadow-xl transition-transform duration-200 ease-in-out lg:hidden',
          isMobileOpen ? 'translate-x-0' : '-translate-x-full',
        )}
      >
        <div className="flex h-16 shrink-0 items-center justify-between border-b px-4">
          <NavLink
            to="/dashboard"
            onClick={handleNavigation}
            className="flex items-center gap-2 text-lg font-semibold tracking-tight"
          >
            <Sparkles className="size-5 text-primary" />
            <span>{appConfig.appName}</span>
          </NavLink>

          <Button
            type="button"
            variant="ghost"
            size="icon"
            aria-label="Close navigation menu"
            onClick={onMobileClose}
          >
            <X />
          </Button>
        </div>

        {navigation}
      </aside>
    </>
  )
}

export default AppSidebar
