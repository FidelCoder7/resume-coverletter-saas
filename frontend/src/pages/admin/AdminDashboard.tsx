import { useState } from 'react'
import {
  Activity,
  Bot,
  CircleDollarSign,
  FileText,
  Mail,
  ShieldCheck,
  UserCheck,
  Users,
} from 'lucide-react'

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import AdminAuditActivityChart from '@/features/admin/components/dashboard/AdminAuditActivityChart'
import AdminDistributions from '@/features/admin/components/dashboard/AdminDistributions'
import AdminMetricCard from '@/features/admin/components/dashboard/AdminMetricCard'
import AdminRegistrationChart from '@/features/admin/components/dashboard/AdminRegistrationChart'
import AdminRevenueSummary from '@/features/admin/components/dashboard/AdminRevenueSummary'
import {
  useAdminMetrics,
  useAdminMetricsTimeSeries,
} from '@/features/admin/hooks/use_admin_metrics'

const CHART_PERIODS = [7, 30, 90] as const

type ChartPeriod = (typeof CHART_PERIODS)[number]

function formatNumber(value: number | undefined) {
  return (value ?? 0).toLocaleString()
}

function formatPercentage(
  numerator: number | undefined,
  denominator: number | undefined,
) {
  if (!numerator || !denominator) {
    return '0%'
  }

  return `${((numerator / denominator) * 100).toFixed(1)}%`
}

function formatLatency(value: number | null | undefined) {
  if (value === null || value === undefined) {
    return 'N/A'
  }

  return `${value.toLocaleString(undefined, {
    maximumFractionDigits: 1,
  })} ms`
}

function AdminDashboard() {
  const [chartPeriod, setChartPeriod] = useState<ChartPeriod>(30)

  const { data: metrics, isPending, isError } = useAdminMetrics()

  const {
    data: timeSeries,
    isPending: isTimeSeriesPending,
    isError: isTimeSeriesError,
  } = useAdminMetricsTimeSeries(chartPeriod)

  if (isError) {
    return (
      <section className="mx-auto w-full max-w-7xl space-y-6">
        <div>
          <h2 className="text-2xl font-semibold tracking-tight sm:text-3xl">
            Admin Dashboard
          </h2>

          <p className="mt-2 text-sm text-muted-foreground">
            Monitor platform activity, users, subscriptions, payments, and AI
            usage.
          </p>
        </div>

        <Card>
          <CardContent className="flex min-h-48 flex-col items-center justify-center text-center">
            <Activity className="size-8 text-destructive" />

            <h3 className="mt-3 text-sm font-semibold">
              Unable to load dashboard metrics
            </h3>

            <p className="mt-1 max-w-md text-sm text-muted-foreground">
              We couldn't retrieve the latest administrative metrics. Please try
              again later.
            </p>
          </CardContent>
        </Card>
      </section>
    )
  }

  const aiUsage = metrics?.ai_usage

  return (
    <section className="mx-auto w-full max-w-7xl space-y-8">
      <div>
        <p className="text-sm font-medium text-primary">Administration</p>

        <h2 className="mt-1 text-2xl font-semibold tracking-tight sm:text-3xl">
          Admin Dashboard
        </h2>

        <p className="mt-2 max-w-3xl text-muted-foreground">
          Monitor users, subscriptions, payments, AI usage, and overall platform
          activity.
        </p>
      </div>

      <section>
        <div className="mb-4">
          <h3 className="text-lg font-semibold">Platform Overview</h3>

          <p className="mt-1 text-sm text-muted-foreground">
            High-level statistics across the application.
          </p>
        </div>

        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <AdminMetricCard
            title="Total Users"
            value={formatNumber(metrics?.users.total_users)}
            description="Registered platform users"
            icon={Users}
            isLoading={isPending}
          />

          <AdminMetricCard
            title="Active Users"
            value={formatNumber(metrics?.users.active_users)}
            description="Currently active accounts"
            icon={UserCheck}
            isLoading={isPending}
          />

          <AdminMetricCard
            title="Administrators"
            value={formatNumber(metrics?.users.total_admins)}
            description="Users with admin access"
            icon={ShieldCheck}
            isLoading={isPending}
          />

          <AdminMetricCard
            title="Audit Logs"
            value={formatNumber(metrics?.total_audit_logs)}
            description="Recorded administrative events"
            icon={Activity}
            isLoading={isPending}
          />
        </div>
      </section>

      <section>
        <div className="mb-4">
          <h3 className="text-lg font-semibold">Content & AI</h3>

          <p className="mt-1 text-sm text-muted-foreground">
            Resume, cover letter, and AI activity across the platform.
          </p>
        </div>

        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <AdminMetricCard
            title="Resumes"
            value={formatNumber(metrics?.content.total_resumes)}
            description="Total resumes created"
            icon={FileText}
            isLoading={isPending}
          />

          <AdminMetricCard
            title="Generated Resumes"
            value={formatNumber(metrics?.content.generated_resumes)}
            description="AI-generated resumes"
            icon={FileText}
            isLoading={isPending}
          />

          <AdminMetricCard
            title="Cover Letters"
            value={formatNumber(metrics?.content.total_cover_letters)}
            description="Total cover letters"
            icon={Mail}
            isLoading={isPending}
          />

          <AdminMetricCard
            title="AI Requests"
            value={formatNumber(aiUsage?.total_requests)}
            description="Total recorded AI requests"
            icon={Bot}
            isLoading={isPending}
          />
        </div>
      </section>

      <section>
        <div className="mb-4">
          <h3 className="text-lg font-semibold">AI Usage</h3>

          <p className="mt-1 text-sm text-muted-foreground">
            Aggregate AI request performance and consumption.
          </p>
        </div>

        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <AdminMetricCard
            title="Success Rate"
            value={formatPercentage(
              aiUsage?.successful_requests,
              aiUsage?.total_requests,
            )}
            description="Successful AI requests"
            icon={ShieldCheck}
            isLoading={isPending}
          />

          <AdminMetricCard
            title="Failed Requests"
            value={formatNumber(aiUsage?.failed_requests)}
            description="Recorded failed AI requests"
            icon={Activity}
            isLoading={isPending}
          />

          <AdminMetricCard
            title="Total Tokens"
            value={formatNumber(aiUsage?.total_tokens)}
            description="Recorded AI tokens"
            icon={Bot}
            isLoading={isPending}
          />

          <AdminMetricCard
            title="Average Latency"
            value={formatLatency(aiUsage?.average_latency_ms)}
            description="Average AI request latency"
            icon={Activity}
            isLoading={isPending}
          />
        </div>
      </section>

      <AdminDistributions metrics={metrics} isLoading={isPending} />

      <AdminRevenueSummary revenue={metrics?.revenue} isLoading={isPending} />

      <section>
        <Card>
          <CardHeader>
            <CardTitle>Payment & Platform Activity</CardTitle>

            <CardDescription>
              Aggregate activity counts reported by the administrative metrics
              service.
            </CardDescription>
          </CardHeader>

          <CardContent>
            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
              <div>
                <p className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                  Transactions
                </p>

                <p className="mt-1 text-xl font-semibold">
                  {isPending
                    ? '...'
                    : formatNumber(metrics?.revenue.total_transactions)}
                </p>

                <p className="mt-1 text-xs text-muted-foreground">
                  Total payment transactions
                </p>
              </div>

              <div>
                <p className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                  Active Subscriptions
                </p>

                <p className="mt-1 text-xl font-semibold">
                  {isPending
                    ? '...'
                    : formatNumber(metrics?.subscriptions.active_subscriptions)}
                </p>

                <p className="mt-1 text-xs text-muted-foreground">
                  Currently active subscriptions
                </p>
              </div>

              <div>
                <p className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                  Platform AI Requests
                </p>

                <p className="mt-1 text-xl font-semibold">
                  {isPending
                    ? '...'
                    : formatNumber(metrics?.platform.total_ai_requests)}
                </p>

                <p className="mt-1 text-xs text-muted-foreground">
                  Requests recorded platform-wide
                </p>
              </div>

              <div>
                <p className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                  Revenue Currencies
                </p>

                <p className="mt-1 flex items-center gap-2 text-xl font-semibold">
                  <CircleDollarSign className="size-5 text-primary" />

                  {isPending
                    ? '...'
                    : Object.keys(
                        metrics?.revenue.total_revenue_by_currency ?? {},
                      ).length}
                </p>

                <p className="mt-1 text-xs text-muted-foreground">
                  Currencies with recorded revenue
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </section>

      <section>
        <div className="mb-4 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <h3 className="text-lg font-semibold">Platform Trends</h3>

            <p className="mt-1 text-sm text-muted-foreground">
              Historical registration and administrative activity.
            </p>
          </div>

          <div
            className="flex w-full rounded-lg border p-1 sm:w-auto"
            aria-label="Chart period"
            role="group"
          >
            {CHART_PERIODS.map((period) => {
              const isActive = chartPeriod === period

              return (
                <button
                  key={period}
                  type="button"
                  aria-pressed={isActive}
                  onClick={() => setChartPeriod(period)}
                  className={`flex-1 rounded-md px-3 py-1.5 text-sm font-medium transition-colors sm:flex-none ${
                    isActive
                      ? 'bg-primary text-primary-foreground'
                      : 'text-muted-foreground hover:bg-muted hover:text-foreground'
                  }`}
                >
                  {period} days
                </button>
              )
            })}
          </div>
        </div>

        <div className="grid gap-4 lg:grid-cols-2">
          <AdminRegistrationChart
            data={timeSeries?.registrations}
            isLoading={isTimeSeriesPending}
            isError={isTimeSeriesError}
          />

          <AdminAuditActivityChart
            data={timeSeries?.audit_activity}
            isLoading={isTimeSeriesPending}
            isError={isTimeSeriesError}
          />
        </div>
      </section>
    </section>
  )
}

export default AdminDashboard
