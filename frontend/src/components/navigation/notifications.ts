export interface AppNotification {
  id: string
  title: string
  message: string
  createdAt: string
  read: boolean
}

export const mockNotifications: AppNotification[] = []
