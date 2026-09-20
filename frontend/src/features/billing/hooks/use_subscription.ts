import { useQuery } from '@tanstack/react-query'

import {
  getSubscriptionLimits,
  getSubscriptionUsage,
} from '@/features/billing/api/subscription_api'

export const subscriptionQueryKeys = {
  all: ['subscriptions'] as const,

  limits: () => [...subscriptionQueryKeys.all, 'limits'] as const,

  usage: () => [...subscriptionQueryKeys.all, 'usage'] as const,
}

export function useSubscriptionLimits() {
  return useQuery({
    queryKey: subscriptionQueryKeys.limits(),
    queryFn: getSubscriptionLimits,
  })
}

export function useSubscriptionUsage() {
  return useQuery({
    queryKey: subscriptionQueryKeys.usage(),
    queryFn: getSubscriptionUsage,
  })
}
