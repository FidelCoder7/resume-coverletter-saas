import { Activity, Clock3, Coins, MessageSquare, XCircle } from 'lucide-react'

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import AdminAnalyticsDistribution from '@/features/admin/components/analytics/AdminAnalyticsDistribution'
import AdminAnalyticsPeriodSelector, {
  type AdminAnalyticsPeriod,
} from '@/features/admin/components/analytics/AdminAnalyticsPeriodSelector'
import AdminAICostActivityChart from '@/features/admin/components/analytics/AdminAICostActivityChart'
import AdminAIRequestActivityChart from '@/features/admin/components/analytics/AdminAIRequestActivityChart'
import AdminAITokenActivityChart from '@/features/admin/components/analytics/AdminAITokenActivityChart'
import AdminMetricCard from '@/features/admin/components/dashboard/AdminMetricCard'
import type { AdminAIAnalyticsResponse } from '@/features/admin/types'

interface AdminAIAnalyticsProps {
  data: AdminAIAnalyticsResponse | undefined
  isLoading: boolean
  period: AdminAnalyticsPeriod
  onPeriodChange: (period: AdminAnalyticsPeriod) => void
}

const featureLabels: Record<string, string> = {
  cover_letter_generation: 'Cover Letter Generation',
  cover_letter_regeneration: 'Cover Letter Regeneration',
  resume_generation: 'Resume Generation',
  ats_optimization: 'ATS Optimization',
}

const statusLabels: Record<string, string> = {
  success: 'Successful',
  failed: 'Failed',
  cancelled: 'Cancelled',
}

function formatLabel(value: string, labels: Record<string, string>) {
  return (
    labels[value] ??
    value
      .replaceAll('_', ' ')
      .replace(/\b\w/g, (character) => character.toUpperCase())
  )
}

function formatCost(value: string) {
  const amount = Number(value)

  if (!Number.isFinite(amount)) {
    return value
  }

  return amount.toLocaleString(undefined, {
    minimumFractionDigits: 0,
    maximumFractionDigits: 6,
  })
}

function AdminAIAnalytics({
  data,
  isLoading,
  period,
  onPeriodChange,
}: AdminAIAnalyticsProps) {
  const featureRequestDistribution = Object.entries(
    data?.requests_by_feature ?? {},
  ).map(([key, value]) => ({
    key,
    label: formatLabel(key, featureLabels),
    value,
  }))

  const featureTokenDistribution = Object.entries(
    data?.tokens_by_feature ?? {},
  ).map(([key, value]) => ({
    key,
    label: formatLabel(key, featureLabels),
    value,
  }))

  const statusDistribution = Object.entries(data?.requests_by_status ?? {}).map(
    ([key, value]) => ({
      key,
      label: formatLabel(key, statusLabels),
      value,
    }),
  )

  return (
    <div className="space-y-6">
      <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
        <div>
          <h2 className="text-lg font-semibold">AI Usage Analytics</h2>

          <p className="mt-1 text-sm text-muted-foreground">
            Monitor AI requests, token consumption, estimated cost, and request
            performance across the selected period.
          </p>
        </div>

        <AdminAnalyticsPeriodSelector
          value={period}
          onChange={onPeriodChange}
          disabled={isLoading}
        />
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <AdminMetricCard
          title="AI Requests"
          value={data?.total_requests ?? 0}
          description={`AI requests during the last ${period} days.`}
          icon={MessageSquare}
          isLoading={isLoading}
        />

        <AdminMetricCard
          title="Successful"
          value={data?.successful_requests ?? 0}
          description="AI requests completed successfully."
          icon={Activity}
          isLoading={isLoading}
        />

        <AdminMetricCard
          title="Failed"
          value={data?.failed_requests ?? 0}
          description="AI requests that failed."
          icon={XCircle}
          isLoading={isLoading}
        />

        <AdminMetricCard
          title="Cancelled"
          value={data?.cancelled_requests ?? 0}
          description="AI requests cancelled before completion."
          icon={XCircle}
          isLoading={isLoading}
        />
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <AdminMetricCard
          title="Total Tokens"
          value={data?.total_tokens ?? 0}
          description="Total AI tokens consumed during the selected period."
          icon={Coins}
          isLoading={isLoading}
        />

        <AdminMetricCard
          title="Estimated Cost"
          value={formatCost(data?.estimated_cost ?? '0')}
          description="Estimated AI processing cost for the selected period."
          icon={Coins}
          isLoading={isLoading}
        />

        <AdminMetricCard
          title="Average Latency"
          value={
            data?.average_latency_ms === null ||
            data?.average_latency_ms === undefined
              ? 'N/A'
              : `${Math.round(data.average_latency_ms)} ms`
          }
          description="Average processing latency for AI requests."
          icon={Clock3}
          isLoading={isLoading}
        />
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <AdminAnalyticsDistribution
          title="Requests by Feature"
          description="AI requests grouped by the feature that generated them."
          items={featureRequestDistribution}
          isLoading={isLoading}
        />

        <AdminAnalyticsDistribution
          title="Requests by Status"
          description="AI requests grouped by their final request status."
          items={statusDistribution}
          isLoading={isLoading}
        />

        <AdminAnalyticsDistribution
          title="Tokens by Feature"
          description="AI token consumption grouped by feature."
          items={featureTokenDistribution}
          isLoading={isLoading}
        />

        <Card>
          <CardHeader>
            <CardTitle>AI Performance</CardTitle>
          </CardHeader>

          <CardContent>
            <div className="grid gap-4 sm:grid-cols-2">
              <div className="rounded-lg border p-4">
                <p className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                  Success Rate
                </p>

                {isLoading ? (
                  <div
                    className="mt-2 h-7 w-20 animate-pulse rounded bg-muted"
                    aria-label="Loading success rate"
                  />
                ) : (
                  <p className="mt-2 text-2xl font-semibold tracking-tight">
                    {data && data.total_requests > 0
                      ? `${((data.successful_requests / data.total_requests) * 100).toFixed(1)}%`
                      : '0.0%'}
                  </p>
                )}

                <p className="mt-1 text-xs text-muted-foreground">
                  Successful requests as a percentage of all requests.
                </p>
              </div>

              <div className="rounded-lg border p-4">
                <p className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                  Tokens per Request
                </p>

                {isLoading ? (
                  <div
                    className="mt-2 h-7 w-20 animate-pulse rounded bg-muted"
                    aria-label="Loading tokens per request"
                  />
                ) : (
                  <p className="mt-2 text-2xl font-semibold tracking-tight">
                    {data && data.total_requests > 0
                      ? Math.round(
                          data.total_tokens / data.total_requests,
                        ).toLocaleString()
                      : '0'}
                  </p>
                )}

                <p className="mt-1 text-xs text-muted-foreground">
                  Average token consumption per AI request.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <AdminAIRequestActivityChart
        data={data?.request_activity ?? []}
        isLoading={isLoading}
      />

      <AdminAITokenActivityChart
        data={data?.token_activity ?? []}
        isLoading={isLoading}
      />

      <AdminAICostActivityChart
        data={data?.cost_activity ?? []}
        isLoading={isLoading}
      />
    </div>
  )
}

export default AdminAIAnalytics
