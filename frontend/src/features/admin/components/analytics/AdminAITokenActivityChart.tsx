import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import type { AdminAIAnalyticsTimeSeriesPoint } from '@/features/admin/types'

interface AdminAITokenActivityChartProps {
  data: AdminAIAnalyticsTimeSeriesPoint[]
  isLoading: boolean
}

function formatDate(value: string) {
  return new Intl.DateTimeFormat(undefined, {
    month: 'short',
    day: 'numeric',
  }).format(new Date(`${value}T00:00:00`))
}

function formatTokens(value: number) {
  return value.toLocaleString()
}

function AdminAITokenActivityChart({
  data,
  isLoading,
}: AdminAITokenActivityChartProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>AI Token Activity</CardTitle>

        <CardDescription>
          Daily token consumption during the selected period.
        </CardDescription>
      </CardHeader>

      <CardContent>
        {isLoading ? (
          <div
            className="h-72 w-full animate-pulse rounded-lg bg-muted"
            aria-label="Loading AI token activity"
          />
        ) : data.length === 0 ? (
          <div className="flex h-72 items-center justify-center rounded-lg border border-dashed text-center">
            <p className="text-sm text-muted-foreground">
              No AI token activity was recorded for this period.
            </p>
          </div>
        ) : (
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart
                data={data}
                margin={{ top: 8, right: 8, left: 8, bottom: 8 }}
              >
                <CartesianGrid strokeDasharray="3 3" />

                <XAxis
                  dataKey="date"
                  tickFormatter={formatDate}
                  tickLine={false}
                  axisLine={false}
                  minTickGap={24}
                />

                <YAxis
                  tickFormatter={formatTokens}
                  tickLine={false}
                  axisLine={false}
                  width={64}
                />

                <Tooltip
                  labelFormatter={(value) => formatDate(String(value))}
                  formatter={(value) => [formatTokens(Number(value)), 'Tokens']}
                />

                <Line
                  type="monotone"
                  dataKey="count"
                  name="Tokens"
                  stroke="currentColor"
                  strokeWidth={2}
                  dot={false}
                  className="text-primary"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}
      </CardContent>
    </Card>
  )
}

export default AdminAITokenActivityChart
