import { Activity } from 'lucide-react'
import { useState } from 'react'

import { Card, CardContent } from '@/components/ui/card'
import AdminAIAnalytics from '@/features/admin/components/analytics/AdminAIAnalytics'
import type { AdminAnalyticsPeriod } from '@/features/admin/components/analytics/AdminAnalyticsPeriodSelector'
import { useAdminAIAnalytics } from '@/features/admin/hooks/use_admin_analytics'
import { getApiErrorMessage } from '@/utils/api_error'

function AdminAIAnalyticsPage() {
  const [period, setPeriod] = useState<AdminAnalyticsPeriod>(30)

  const { data, isLoading, isError, error } = useAdminAIAnalytics(period)

  return (
    <div className="mx-auto w-full max-w-7xl space-y-6">
      <section>
        <p className="text-sm font-medium text-primary">Administration</p>

        <h2 className="mt-1 text-2xl font-semibold tracking-tight sm:text-3xl">
          AI Usage Analytics
        </h2>

        <p className="mt-2 max-w-3xl text-muted-foreground">
          Monitor AI requests, token consumption, estimated cost, feature usage,
          and request performance across the selected period.
        </p>
      </section>

      {isError ? (
        <Card>
          <CardContent className="flex min-h-48 flex-col items-center justify-center text-center">
            <Activity className="size-8 text-destructive" />

            <h3 className="mt-3 text-sm font-semibold">
              Unable to load AI analytics
            </h3>

            <p className="mt-1 max-w-md text-sm text-muted-foreground">
              {getApiErrorMessage(error)}
            </p>
          </CardContent>
        </Card>
      ) : (
        <AdminAIAnalytics
          data={data}
          isLoading={isLoading}
          period={period}
          onPeriodChange={setPeriod}
        />
      )}
    </div>
  )
}

export default AdminAIAnalyticsPage
