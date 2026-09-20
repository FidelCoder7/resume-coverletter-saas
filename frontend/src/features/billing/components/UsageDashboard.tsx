import { AlertCircle, CalendarDays, Loader2 } from 'lucide-react'

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import UsageFeatureCard from '@/features/billing/components/UsageFeatureCard'
import {
  useSubscriptionLimits,
  useSubscriptionUsage,
} from '@/features/billing/hooks/use_subscription'

function formatDate(value: string) {
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: 'medium',
  }).format(new Date(value))
}

function UsageDashboard() {
  const {
    data: limitsData,
    isPending: limitsPending,
    isError: limitsError,
  } = useSubscriptionLimits()

  const {
    data: usageData,
    isPending: usagePending,
    isError: usageError,
  } = useSubscriptionUsage()

  const isPending = limitsPending || usagePending
  const hasError = limitsError || usageError

  if (isPending) {
    return (
      <Card>
        <CardContent className="flex min-h-48 items-center justify-center">
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <Loader2 className="size-4 animate-spin" />
            Loading subscription usage...
          </div>
        </CardContent>
      </Card>
    )
  }

  if (hasError || !usageData || !limitsData) {
    return (
      <Card>
        <CardContent className="flex min-h-48 flex-col items-center justify-center text-center">
          <AlertCircle className="size-8 text-destructive" />

          <h3 className="mt-3 text-sm font-semibold">
            Unable to load subscription usage
          </h3>

          <p className="mt-1 max-w-md text-sm text-muted-foreground">
            We couldn't retrieve your current subscription limits and usage.
            Please try again later.
          </p>
        </CardContent>
      </Card>
    )
  }

  const limitsByFeature = new Map(
    limitsData.limits.map((limit) => [limit.feature, limit]),
  )

  const usage = usageData.features.map((featureUsage) => {
    const configuredLimit = limitsByFeature.get(featureUsage.feature)

    return {
      ...featureUsage,
      limit_value: configuredLimit?.limit_value ?? featureUsage.limit_value,
    }
  })

  return (
    <section className="space-y-4">
      <div>
        <h3 className="text-lg font-semibold">Usage Dashboard</h3>

        <p className="mt-1 text-sm text-muted-foreground">
          Monitor your AI feature usage for the current subscription period.
        </p>
      </div>

      <Card>
        <CardHeader>
          <div className="flex items-start gap-3">
            <div className="flex size-9 shrink-0 items-center justify-center rounded-lg bg-primary/10 text-primary">
              <CalendarDays className="size-5" />
            </div>

            <div>
              <CardTitle className="text-base">
                Current billing period
              </CardTitle>

              <CardDescription className="mt-1">
                Your usage resets according to your subscription billing period.
              </CardDescription>
            </div>
          </div>
        </CardHeader>

        <CardContent>
          <div className="grid gap-4 sm:grid-cols-2">
            <div>
              <p className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                Period starts
              </p>

              <p className="mt-1 text-sm font-medium">
                {formatDate(usageData.period_start)}
              </p>
            </div>

            <div>
              <p className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                Period ends
              </p>

              <p className="mt-1 text-sm font-medium">
                {formatDate(usageData.period_end)}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      <div className="grid gap-4 md:grid-cols-2">
        {usage.map((featureUsage) => (
          <UsageFeatureCard key={featureUsage.feature} usage={featureUsage} />
        ))}
      </div>
    </section>
  )
}

export default UsageDashboard
