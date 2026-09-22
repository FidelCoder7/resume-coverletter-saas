import { useEffect, useState } from 'react'
import { Outlet } from 'react-router-dom'

import AdminHeader from '@/features/admin/components/AdminHeader'
import AdminSidebar from '@/features/admin/components/AdminSidebar'

function AdminLayout() {
  const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false)

  const openMobileSidebar = () => {
    setIsMobileSidebarOpen(true)
  }

  const closeMobileSidebar = () => {
    setIsMobileSidebarOpen(false)
  }

  useEffect(() => {
    if (!isMobileSidebarOpen) {
      return
    }

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        closeMobileSidebar()
      }
    }

    window.addEventListener('keydown', handleKeyDown)

    return () => {
      window.removeEventListener('keydown', handleKeyDown)
    }
  }, [isMobileSidebarOpen])

  return (
    <div className="flex min-h-screen bg-background text-foreground">
      <AdminSidebar
        isMobileOpen={isMobileSidebarOpen}
        onMobileClose={closeMobileSidebar}
      />

      <div className="flex min-w-0 flex-1 flex-col">
        <AdminHeader onMenuClick={openMobileSidebar} />

        <main className="flex-1 overflow-y-auto p-4 sm:p-6">
          <Outlet />
        </main>
      </div>
    </div>
  )
}

export default AdminLayout
