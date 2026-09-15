import { Activity, Clock3, Coins, MessageSquare, XCircle } from 'lucide-react'

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import type { AIUsageSummary } from '@/features/ai_usage/types'

interface AIUsageSummaryCardsProps {
  summary: AIUsageSummary
}

function AIUsageSummaryCards({ summary }: AIUsageSummaryCardsProps) {
  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
      <SummaryCard
        icon={MessageSquare}
        label="Total Requests"
        value={summary.total_requests.toLocaleString()}
      />

      <SummaryCard
        icon={Activity}
        label="Successful"
        value={summary.successful_requests.toLocaleString()}
      />

      <SummaryCard
        icon={XCircle}
        label="Failed"
        value={summary.failed_requests.toLocaleString()}
      />

      <SummaryCard
        icon={Coins}
        label="Total Tokens"
        value={summary.total_tokens.toLocaleString()}
      />

      <SummaryCard
        icon={Clock3}
        label="Avg. Latency"
        value={
          summary.average_latency_ms === null
            ? 'N/A'
            : `${Math.round(summary.average_latency_ms)} ms`
        }
      />
    </div>
  )
}

interface SummaryCardProps {
  icon: typeof Activity
  label: string
  value: string
}

function SummaryCard({ icon: Icon, label, value }: SummaryCardProps) {
  return (
    <Card>
      <CardHeader className="pb-3">
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <Icon className="size-4" />

          <CardTitle className="text-sm font-medium">{label}</CardTitle>
        </div>
      </CardHeader>

      <CardContent>
        <p className="text-2xl font-semibold tracking-tight">{value}</p>
      </CardContent>
    </Card>
  )
}

export default AIUsageSummaryCards
