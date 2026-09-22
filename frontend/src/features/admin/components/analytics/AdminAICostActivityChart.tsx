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
import type { AdminAICostTimeSeriesPoint } from '@/features/admin/types'

interface AdminAICostActivityChartProps {
  currency?: string
  data: AdminAICostTimeSeriesPoint[]
  isLoading: boolean
}

function formatDate(value: string) {
  return new Intl.DateTimeFormat(undefined, {
    month: 'short',
    day: 'numeric',
  }).format(new Date(`${value}T00:00:00`))
}

function formatAmount(value: string | number, currency: string) {
  const amount = Number(value)

  if (!Number.isFinite(amount)) {
    return `${currency} ${value}`
  }

  return new Intl.NumberFormat(undefined, {
    style: 'currency',
    currency,
    maximumFractionDigits: 6,
  }).format(amount)
}

function AdminAICostActivityChart({
  currency = 'USD',
  data,
  isLoading,
}: AdminAICostActivityChartProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>AI Cost Activity</CardTitle>

        <CardDescription>
          Daily estimated AI cost during the selected period.
        </CardDescription>
      </CardHeader>

      <CardContent>
        {isLoading ? (
          <div
            className="h-72 w-full animate-pulse rounded-lg bg-muted"
            aria-label="Loading AI cost activity"
          />
        ) : data.length === 0 ? (
          <div className="flex h-72 items-center justify-center rounded-lg border border-dashed text-center">
            <p className="text-sm text-muted-foreground">
              No AI cost activity was recorded for this period.
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
                  tickFormatter={(value) =>
                    formatAmount(Number(value), currency)
                  }
                  tickLine={false}
                  axisLine={false}
                  width={72}
                />

                <Tooltip
                  labelFormatter={(value) => formatDate(String(value))}
                  formatter={(value) => [
                    formatAmount(Number(value), currency),
                    'Estimated Cost',
                  ]}
                />

                <Line
                  type="monotone"
                  dataKey="amount"
                  name="Estimated Cost"
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

export default AdminAICostActivityChart
