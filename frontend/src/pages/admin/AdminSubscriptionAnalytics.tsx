import { Activity } from 'lucide-react'

import { Card, CardContent } from '@/components/ui/card'
import AdminSubscriptionAnalytics from '@/features/admin/components/analytics/AdminSubscriptionAnalytics'
import { useAdminSubscriptionAnalytics } from '@/features/admin/hooks/use_admin_analytics'
import { getApiErrorMessage } from '@/utils/api_error'

function AdminSubscriptionAnalyticsPage() {
  const { data, isLoading, isError, error } = useAdminSubscriptionAnalytics()

  return (
    <div className="mx-auto w-full max-w-7xl space-y-6">
      <section>
        <p className="text-sm font-medium text-primary">Administration</p>

        <h2 className="mt-1 text-2xl font-semibold tracking-tight sm:text-3xl">
          Subscription Analytics
        </h2>

        <p className="mt-2 max-w-3xl text-muted-foreground">
          Monitor the current distribution of Free and Pro subscriptions across
          the platform.
        </p>
      </section>

      {isError ? (
        <Card>
          <CardContent className="flex min-h-48 flex-col items-center justify-center text-center">
            <Activity className="size-8 text-destructive" />

            <h3 className="mt-3 text-sm font-semibold">
              Unable to load subscription analytics
            </h3>

            <p className="mt-1 max-w-md text-sm text-muted-foreground">
              {getApiErrorMessage(error)}
            </p>
          </CardContent>
        </Card>
      ) : (
        <AdminSubscriptionAnalytics data={data} isLoading={isLoading} />
      )}
    </div>
  )
}

export default AdminSubscriptionAnalyticsPage
