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

export type AdminAuditAction =
  | 'user_suspended'
  | 'user_activated'
  | 'user_deleted'
  | 'user_restored'
  | 'user_role_changed'
  | 'user_subscription_changed'

export interface AdminAuditLog {
  id: string
  admin_id: string
  target_user_id: string
  action: AdminAuditAction
  reason: string | null
  event_metadata: Record<string, unknown> | null
  created_at: string
}

export interface AdminAuditLogListResponse {
  items: AdminAuditLog[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

export interface AdminAuditLogListParams {
  page?: number
  page_size?: number
  action?: AdminAuditAction
  admin_id?: string
  target_user_id?: string
  created_after?: string
  created_before?: string
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

export interface AdminAnalyticsDaysParams {
  days?: number
}

export interface AdminSubscriptionAnalyticsResponse {
  total_users: number
  free_users: number
  pro_users: number
  active_subscriptions: number
}

export interface AdminPaymentAnalyticsTimeSeriesPoint {
  date: string
  count: number
}

export interface AdminPaymentRevenueTimeSeriesPoint {
  date: string
  amount: string
}

export interface AdminPaymentAnalyticsResponse {
  days: number
  total_transactions: number
  completed_transactions: number
  pending_transactions: number
  failed_transactions: number
  cancelled_transactions: number
  expired_transactions: number
  total_revenue_by_currency: Record<string, string>
  transactions_by_plan: Record<string, number>
  transactions_by_type: Record<string, number>
  transactions_by_provider: Record<string, number>
  transactions_by_payment_method: Record<string, number>
  transaction_activity: AdminPaymentAnalyticsTimeSeriesPoint[]
  revenue_activity: Record<string, AdminPaymentRevenueTimeSeriesPoint[]>
}

export interface AdminAIAnalyticsTimeSeriesPoint {
  date: string
  count: number
}

export interface AdminAICostTimeSeriesPoint {
  date: string
  amount: string
}

export interface AdminAIAnalyticsResponse {
  days: number
  total_requests: number
  successful_requests: number
  failed_requests: number
  cancelled_requests: number
  total_tokens: number
  estimated_cost: string
  average_latency_ms: number | null
  requests_by_feature: Record<string, number>
  requests_by_status: Record<string, number>
  tokens_by_feature: Record<string, number>
  request_activity: AdminAIAnalyticsTimeSeriesPoint[]
  token_activity: AdminAIAnalyticsTimeSeriesPoint[]
  cost_activity: AdminAICostTimeSeriesPoint[]
}
