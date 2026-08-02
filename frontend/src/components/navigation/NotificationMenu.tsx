import { Bell } from 'lucide-react'
import { useState } from 'react'

import { Button } from '@/components/ui/button'
import { mockNotifications } from '@/components/navigation/notifications'

function NotificationMenu() {
  const [isOpen, setIsOpen] = useState(false)

  const unreadCount = mockNotifications.filter(
    (notification) => !notification.read,
  ).length

  return (
    <div className="relative">
      <Button
        type="button"
        variant="ghost"
        size="icon"
        aria-expanded={isOpen}
        aria-haspopup="menu"
        aria-label={
          unreadCount > 0
            ? `Notifications, ${unreadCount} unread`
            : 'Notifications'
        }
        title="Notifications"
        onClick={() => {
          setIsOpen((current) => !current)
        }}
      >
        <Bell />

        {unreadCount > 0 && (
          <span
            aria-hidden="true"
            className="absolute top-1.5 right-1.5 flex size-2 rounded-full bg-destructive ring-2 ring-background"
          />
        )}
      </Button>

      {isOpen && (
        <>
          <button
            type="button"
            className="fixed inset-0 z-40 cursor-default"
            aria-label="Close notifications"
            onClick={() => {
              setIsOpen(false)
            }}
          />

          <div
            role="menu"
            aria-label="Notifications"
            className="absolute right-0 z-50 mt-2 w-80 max-w-[calc(100vw-2rem)] overflow-hidden rounded-xl border bg-card text-card-foreground shadow-lg"
          >
            <div className="flex items-center justify-between border-b px-4 py-3">
              <div>
                <h2 className="text-sm font-semibold">Notifications</h2>

                <p className="text-xs text-muted-foreground">
                  Stay up to date with your account activity.
                </p>
              </div>
            </div>

            {mockNotifications.length === 0 ? (
              <div className="px-4 py-10 text-center">
                <Bell className="mx-auto size-8 text-muted-foreground/50" />

                <p className="mt-3 text-sm font-medium">No notifications</p>

                <p className="mt-1 text-xs text-muted-foreground">
                  You're all caught up.
                </p>
              </div>
            ) : (
              <div className="max-h-96 overflow-y-auto p-2">
                {mockNotifications.map((notification) => (
                  <div
                    key={notification.id}
                    role="menuitem"
                    className="rounded-lg px-3 py-3 transition-colors hover:bg-muted"
                  >
                    <div className="flex items-start gap-3">
                      <span
                        className={
                          notification.read
                            ? 'mt-1.5 size-2 shrink-0 rounded-full bg-muted-foreground/30'
                            : 'mt-1.5 size-2 shrink-0 rounded-full bg-primary'
                        }
                      />

                      <div className="min-w-0">
                        <p className="text-sm font-medium">
                          {notification.title}
                        </p>

                        <p className="mt-1 text-xs text-muted-foreground">
                          {notification.message}
                        </p>

                        <p className="mt-2 text-xs text-muted-foreground">
                          {notification.createdAt}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </>
      )}
    </div>
  )
}

export default NotificationMenu
