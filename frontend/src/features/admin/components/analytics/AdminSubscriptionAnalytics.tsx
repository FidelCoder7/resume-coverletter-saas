import { CreditCard, Users } from 'lucide-react'

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import AdminAnalyticsDistribution from '@/features/admin/components/analytics/AdminAnalyticsDistribution'
import AdminMetricCard from '@/features/admin/components/dashboard/AdminMetricCard'
import type { AdminSubscriptionAnalyticsResponse } from '@/features/admin/types'

interface AdminSubscriptionAnalyticsProps {
  data: AdminSubscriptionAnalyticsResponse | undefined
  isLoading: boolean
}

function AdminSubscriptionAnalytics({
  data,
  isLoading,
}: AdminSubscriptionAnalyticsProps) {
  const distribution = [
    {
      key: 'free',
      label: 'Free',
      value: data?.free_users ?? 0,
    },
    {
      key: 'pro',
      label: 'Pro',
      value: data?.pro_users ?? 0,
    },
  ]

  return (
    <div className="space-y-6">
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <AdminMetricCard
          title="Total Users"
          value={data?.total_users ?? 0}
          description="Users currently represented in the subscription distribution."
          icon={Users}
          isLoading={isLoading}
        />

        <AdminMetricCard
          title="Free Users"
          value={data?.free_users ?? 0}
          description="Users currently assigned to the Free plan."
          icon={Users}
          isLoading={isLoading}
        />

        <AdminMetricCard
          title="Pro Users"
          value={data?.pro_users ?? 0}
          description="Users currently assigned to the Pro plan."
          icon={CreditCard}
          isLoading={isLoading}
        />
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Subscription Overview</CardTitle>
        </CardHeader>

        <CardContent>
          <div className="grid gap-4 sm:grid-cols-2">
            <div className="rounded-lg border p-4">
              <p className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                Active Subscriptions
              </p>

              {isLoading ? (
                <div
                  className="mt-2 h-7 w-20 animate-pulse rounded bg-muted"
                  aria-label="Loading active subscriptions"
                />
              ) : (
                <p className="mt-2 text-2xl font-semibold tracking-tight">
                  {(data?.active_subscriptions ?? 0).toLocaleString()}
                </p>
              )}

              <p className="mt-1 text-xs text-muted-foreground">
                Current users with an active paid subscription.
              </p>
            </div>

            <div className="rounded-lg border p-4">
              <p className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                Pro Share
              </p>

              {isLoading ? (
                <div
                  className="mt-2 h-7 w-20 animate-pulse rounded bg-muted"
                  aria-label="Loading Pro share"
                />
              ) : (
                <p className="mt-2 text-2xl font-semibold tracking-tight">
                  {data && data.total_users > 0
                    ? `${((data.pro_users / data.total_users) * 100).toFixed(1)}%`
                    : '0.0%'}
                </p>
              )}

              <p className="mt-1 text-xs text-muted-foreground">
                Pro users as a percentage of all users.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      <AdminAnalyticsDistribution
        title="Subscription Distribution"
        description="Current users grouped by their subscription plan."
        items={distribution}
        isLoading={isLoading}
      />
    </div>
  )
}

export default AdminSubscriptionAnalytics
