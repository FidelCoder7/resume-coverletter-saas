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

export interface AdminUserMetrics {
  total_users: number
  active_users: number
  suspended_users: number
  deleted_users: number
  verified_users: number
  unverified_users: number
  total_admins: number
}

export interface AdminSubscriptionMetrics {
  free_users: number
  pro_users: number
  active_subscriptions: number
}

export interface AdminRevenueMetrics {
  total_transactions: number
  completed_transactions: number
  pending_transactions: number
  failed_transactions: number
  cancelled_transactions: number
  expired_transactions: number
  total_revenue_by_currency: Record<string, string>
}

export interface AdminAIUsageMetrics {
  total_requests: number
  successful_requests: number
  failed_requests: number
  total_tokens: number
  estimated_cost: string
  average_latency_ms: number | null
}

export interface AdminContentMetrics {
  total_resumes: number
  generated_resumes: number
  total_cover_letters: number
}

export interface AdminPlatformActivityMetrics {
  total_users: number
  total_resumes: number
  total_cover_letters: number
  total_ai_requests: number
  total_payment_transactions: number
  total_audit_logs: number
}

export interface AdminDashboardMetricsResponse {
  users: AdminUserMetrics
  subscriptions: AdminSubscriptionMetrics
  revenue: AdminRevenueMetrics
  ai_usage: AdminAIUsageMetrics
  content: AdminContentMetrics
  platform: AdminPlatformActivityMetrics
  total_audit_logs: number
}

export interface AdminTimeSeriesPoint {
  date: string
  count: number
}

export interface AdminDashboardTimeSeriesResponse {
  days: number
  registrations: AdminTimeSeriesPoint[]
  audit_activity: AdminTimeSeriesPoint[]
}

export interface AdminDashboardTimeSeriesParams {
  days?: number
}
