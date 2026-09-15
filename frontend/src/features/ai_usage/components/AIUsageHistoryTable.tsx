import { CheckCircle2, Clock3, LoaderCircle, XCircle } from 'lucide-react'

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import type {
  AIFeature,
  AIRequestStatus,
  AIUsage,
} from '@/features/ai_usage/types'
import { getApiErrorMessage } from '@/utils/api_error'

interface AIUsageHistoryTableProps {
  usage: AIUsage[]
  isLoading: boolean
  isError: boolean
  error: unknown
}

const featureLabels: Record<AIFeature, string> = {
  resume_generation: 'Resume Generation',
  cover_letter_generation: 'Cover Letter Generation',
  cover_letter_regeneration: 'Cover Letter Regeneration',
  ats_optimization: 'ATS Optimization',
}

function AIUsageHistoryTable({
  usage,
  isLoading,
  isError,
  error,
}: AIUsageHistoryTableProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>AI Request History</CardTitle>

        <CardDescription>
          Individual AI requests recorded for your account.
        </CardDescription>
      </CardHeader>

      <CardContent>
        {isLoading ? (
          <div className="flex items-center justify-center gap-2 py-10 text-sm text-muted-foreground">
            <LoaderCircle className="size-4 animate-spin" />
            Loading AI usage history...
          </div>
        ) : isError ? (
          <div className="rounded-lg border border-destructive/30 bg-destructive/5 px-4 py-3">
            <p className="text-sm text-destructive">
              {getApiErrorMessage(error)}
            </p>
          </div>
        ) : usage.length === 0 ? (
          <div className="flex flex-col items-center justify-center rounded-lg border border-dashed px-6 py-10 text-center">
            <Clock3 className="size-7 text-muted-foreground" />

            <p className="mt-3 text-sm font-medium">No AI requests found</p>

            <p className="mt-1 text-sm text-muted-foreground">
              AI requests made during this period will appear here.
            </p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full min-w-[760px] text-sm">
              <thead>
                <tr className="border-b text-left text-xs text-muted-foreground">
                  <th className="px-4 py-3 font-medium">Feature</th>
                  <th className="px-4 py-3 font-medium">Provider</th>
                  <th className="px-4 py-3 font-medium">Model</th>
                  <th className="px-4 py-3 font-medium">Tokens</th>
                  <th className="px-4 py-3 font-medium">Latency</th>
                  <th className="px-4 py-3 font-medium">Status</th>
                  <th className="px-4 py-3 font-medium">Created</th>
                </tr>
              </thead>

              <tbody>
                {usage.map((record) => (
                  <tr key={record.id} className="border-b last:border-0">
                    <td className="px-4 py-4 font-medium">
                      {featureLabels[record.feature]}
                    </td>

                    <td className="px-4 py-4 text-muted-foreground">
                      {record.provider}
                    </td>

                    <td className="px-4 py-4 text-muted-foreground">
                      {record.model}
                    </td>

                    <td className="px-4 py-4">
                      {record.total_tokens === null
                        ? 'N/A'
                        : record.total_tokens.toLocaleString()}
                    </td>

                    <td className="px-4 py-4">
                      {record.latency_ms === null
                        ? 'N/A'
                        : `${record.latency_ms.toLocaleString()} ms`}
                    </td>

                    <td className="px-4 py-4">
                      <StatusBadge status={record.status} />
                    </td>

                    <td className="whitespace-nowrap px-4 py-4 text-muted-foreground">
                      {formatDate(record.created_at)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </CardContent>
    </Card>
  )
}

interface StatusBadgeProps {
  status: AIRequestStatus
}

function StatusBadge({ status }: StatusBadgeProps) {
  const config: Record<
    AIRequestStatus,
    {
      label: string
      icon: typeof CheckCircle2
      className: string
    }
  > = {
    success: {
      label: 'Success',
      icon: CheckCircle2,
      className: 'border-primary/30 bg-primary/5 text-primary',
    },

    failed: {
      label: 'Failed',
      icon: XCircle,
      className: 'border-destructive/30 bg-destructive/5 text-destructive',
    },

    cancelled: {
      label: 'Cancelled',
      icon: Clock3,
      className: 'border-muted-foreground/30 bg-muted text-muted-foreground',
    },
  }

  const current = config[status]
  const Icon = current.icon

  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-xs font-medium ${current.className}`}
    >
      <Icon className="size-3.5" />
      {current.label}
    </span>
  )
}

function formatDate(value: string) {
  return new Date(value).toLocaleString()
}

export default AIUsageHistoryTable
