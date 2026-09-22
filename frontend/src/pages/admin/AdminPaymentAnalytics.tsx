import { Activity } from 'lucide-react'
import { useState } from 'react'

import { Card, CardContent } from '@/components/ui/card'
import AdminPaymentAnalytics from '@/features/admin/components/analytics/AdminPaymentAnalytics'
import type { AdminAnalyticsPeriod } from '@/features/admin/components/analytics/AdminAnalyticsPeriodSelector'
import { useAdminPaymentAnalytics } from '@/features/admin/hooks/use_admin_analytics'
import { getApiErrorMessage } from '@/utils/api_error'

function AdminPaymentAnalyticsPage() {
  const [period, setPeriod] = useState<AdminAnalyticsPeriod>(30)

  const { data, isLoading, isError, error } = useAdminPaymentAnalytics(period)

  return (
    <div className="mx-auto w-full max-w-7xl space-y-6">
      <section>
        <p className="text-sm font-medium text-primary">Administration</p>

        <h2 className="mt-1 text-2xl font-semibold tracking-tight sm:text-3xl">
          Payment Analytics
        </h2>

        <p className="mt-2 max-w-3xl text-muted-foreground">
          Monitor payment transactions, revenue, providers, payment methods, and
          transaction activity across the selected period.
        </p>
      </section>

      {isError ? (
        <Card>
          <CardContent className="flex min-h-48 flex-col items-center justify-center text-center">
            <Activity className="size-8 text-destructive" />

            <h3 className="mt-3 text-sm font-semibold">
              Unable to load payment analytics
            </h3>

            <p className="mt-1 max-w-md text-sm text-muted-foreground">
              {getApiErrorMessage(error)}
            </p>
          </CardContent>
        </Card>
      ) : (
        <AdminPaymentAnalytics
          data={data}
          isLoading={isLoading}
          period={period}
          onPeriodChange={setPeriod}
        />
      )}
    </div>
  )
}

export default AdminPaymentAnalyticsPage
