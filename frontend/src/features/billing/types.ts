import type { SubscriptionPlan } from '@/types/user'

export type PaymentProvider = 'pesapal'

export type PaymentStatus =
  'pending' | 'completed' | 'failed' | 'cancelled' | 'expired'

export type PaymentMethod = 'mpesa' | 'card' | 'bank' | 'other'

export type BillingTransactionType =
  | 'subscription_purchase'
  | 'subscription_renewal'
  | 'subscription_upgrade'
  | 'subscription_downgrade'

export type SubscriptionLimitPeriod = 'monthly'

export type AIFeature =
  | 'cover_letter_generation'
  | 'cover_letter_regeneration'
  | 'resume_generation'
  | 'ats_optimization'

export interface PaymentInitiationRequest {
  subscription_plan: SubscriptionPlan
  transaction_type?: BillingTransactionType
  payment_method?: PaymentMethod | null
}

export interface PaymentTransaction {
  id: string
  user_id: string
  subscription_plan: SubscriptionPlan
  transaction_type: BillingTransactionType
  provider: PaymentProvider
  provider_order_id: string
  provider_transaction_id: string | null
  amount: string
  currency: string
  payment_method: PaymentMethod | null
  status: PaymentStatus
  failure_reason: string | null
  provider_response: Record<string, unknown> | null
}

export interface PaymentInitiationResponse {
  transaction: PaymentTransaction
  redirect_url: string | null
}

export interface PaymentTransactionListResponse {
  transactions: PaymentTransaction[]
}

export interface PaymentStatusResponse {
  transaction: PaymentTransaction
}

export interface PlanLimit {
  id: string
  subscription_plan: SubscriptionPlan
  feature: AIFeature
  limit_value: number
  period: SubscriptionLimitPeriod
}

export interface PlanLimitListResponse {
  subscription_plan: SubscriptionPlan
  limits: PlanLimit[]
}

export interface FeatureUsage {
  feature: AIFeature
  limit_value: number
  usage: number
  remaining: number
  period: SubscriptionLimitPeriod
}

export interface SubscriptionUsage {
  subscription_plan: SubscriptionPlan
  period_start: string
  period_end: string
  features: FeatureUsage[]
}
