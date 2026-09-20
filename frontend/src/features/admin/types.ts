import type { AccountStatus, SubscriptionPlan, UserRole } from '@/types/user'

export interface AdminAccessResponse {
  message: string
  role: UserRole
}

export interface AdminUserListItem {
  id: string
  email: string
  full_name: string
  role: UserRole
  subscription_plan: SubscriptionPlan
  status: AccountStatus
  is_email_verified: boolean
  last_login_at: string | null
  created_at: string
}

export interface AdminUserDetail extends AdminUserListItem {
  updated_at: string
  deleted_at: string | null
}

export interface AdminUserListResponse {
  items: AdminUserListItem[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

export interface AdminUserListParams {
  page?: number
  page_size?: number
  search?: string
  role?: UserRole
  status?: AccountStatus
  subscription_plan?: SubscriptionPlan
}

export interface AdminUserActionRequest {
  reason?: string
}
