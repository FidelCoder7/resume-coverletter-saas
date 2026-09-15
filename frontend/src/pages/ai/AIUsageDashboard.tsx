import { ArrowLeft, BarChart3, LoaderCircle } from 'lucide-react'
import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'

import { buttonVariants } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import AIFeatureBreakdown from '@/features/ai_usage/components/AIFeatureBreakdown'
import AIUsageHistoryTable from '@/features/ai_usage/components/AIUsageHistoryTable'
import AIUsageSummaryCards from '@/features/ai_usage/components/AIUsageSummaryCards'
import {
  useAIUsage,
  useAIUsageDashboard,
} from '@/features/ai_usage/hooks/use_ai_usage'
import { getApiErrorMessage } from '@/utils/api_error'

function AIUsageDashboard() {
  const initialPeriod = useMemo(() => getDefaultPeriod(), [])

  const [startDate, setStartDate] = useState(initialPeriod.startDate)
  const [endDate, setEndDate] = useState(initialPeriod.endDate)

  const {
    data: dashboard,
    isLoading: isDashboardLoading,
    isError: isDashboardError,
    error: dashboardError,
  } = useAIUsageDashboard(startDate, endDate)

  const {
    data: usage = [],
    isLoading: isUsageLoading,
    isError: isUsageError,
    error: usageError,
  } = useAIUsage()

  const filteredUsage = useMemo(() => {
    const start = new Date(`${startDate}T00:00:00`)
    const end = new Date(`${endDate}T23:59:59.999`)

    return usage.filter((record) => {
      const createdAt = new Date(record.created_at)

      return createdAt >= start && createdAt <= end
    })
  }, [usage, startDate, endDate])

  function handleStartDateChange(value: string) {
    setStartDate(value)
  }

  function handleEndDateChange(value: string) {
    setEndDate(value)
  }

  return (
    <div className="mx-auto w-full max-w-7xl space-y-8">
      <section>
        <Link
          to="/ai"
          className={buttonVariants({
            variant: 'outline',
            size: 'sm',
          })}
        >
          <ArrowLeft />
          Back to AI Workspace
        </Link>

        <div className="mt-6 flex items-center gap-3">
          <div className="flex size-10 items-center justify-center rounded-lg bg-primary/10">
            <BarChart3 className="size-5 text-primary" />
          </div>

          <div>
            <p className="text-sm font-medium text-primary">AI Usage</p>

            <h1 className="text-3xl font-semibold tracking-tight">
              Usage Dashboard
            </h1>
          </div>
        </div>

        <p className="mt-3 max-w-2xl text-sm leading-6 text-muted-foreground">
          Monitor your AI requests, token consumption, feature usage, and
          request performance.
        </p>
      </section>

      <Card>
        <CardHeader>
          <CardTitle>Date Range</CardTitle>

          <CardDescription>
            Select the period you want to analyze.
          </CardDescription>
        </CardHeader>

        <CardContent>
          <div className="grid gap-4 sm:grid-cols-2">
            <div className="space-y-2">
              <label htmlFor="start-date" className="text-sm font-medium">
                Start date
              </label>

              <input
                id="start-date"
                type="date"
                value={startDate}
                max={endDate}
                onChange={(event) => handleStartDateChange(event.target.value)}
                className="flex h-9 w-full rounded-lg border border-input bg-background px-3 text-sm outline-none transition-colors focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/50"
              />
            </div>

            <div className="space-y-2">
              <label htmlFor="end-date" className="text-sm font-medium">
                End date
              </label>

              <input
                id="end-date"
                type="date"
                value={endDate}
                min={startDate}
                onChange={(event) => handleEndDateChange(event.target.value)}
                className="flex h-9 w-full rounded-lg border border-input bg-background px-3 text-sm outline-none transition-colors focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/50"
              />
            </div>
          </div>
        </CardContent>
      </Card>

      {isDashboardLoading ? (
        <div className="flex items-center justify-center gap-2 py-10 text-sm text-muted-foreground">
          <LoaderCircle className="size-4 animate-spin" />
          Loading AI usage dashboard...
        </div>
      ) : isDashboardError ? (
        <Card>
          <CardContent className="pt-6">
            <div className="rounded-lg border border-destructive/30 bg-destructive/5 px-4 py-3">
              <p className="text-sm text-destructive">
                {getApiErrorMessage(dashboardError)}
              </p>
            </div>
          </CardContent>
        </Card>
      ) : dashboard ? (
        <>
          <AIUsageSummaryCards summary={dashboard.summary} />

          <AIFeatureBreakdown features={dashboard.features} />
        </>
      ) : null}

      <AIUsageHistoryTable
        usage={filteredUsage}
        isLoading={isUsageLoading}
        isError={isUsageError}
        error={usageError}
      />
    </div>
  )
}

function getDefaultPeriod() {
  const end = new Date()
  const start = new Date(end)

  start.setDate(start.getDate() - 29)

  return {
    startDate: formatDateInput(start),
    endDate: formatDateInput(end),
  }
}

function formatDateInput(date: Date) {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')

  return `${year}-${month}-${day}`
}

export default AIUsageDashboard
