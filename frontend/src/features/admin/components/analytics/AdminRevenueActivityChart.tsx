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
import type { AdminPaymentRevenueTimeSeriesPoint } from '@/features/admin/types'

interface AdminRevenueActivityChartProps {
  currency: string
  data: AdminPaymentRevenueTimeSeriesPoint[]
  isLoading?: boolean
}

function formatDate(value: string) {
  return new Intl.DateTimeFormat(undefined, {
    month: 'short',
    day: 'numeric',
  }).format(new Date(`${value}T00:00:00`))
}

function formatCurrency(value: number, currency: string) {
  return new Intl.NumberFormat(undefined, {
    style: 'currency',
    currency,
    maximumFractionDigits: 2,
  }).format(value)
}

function AdminRevenueActivityChart({
  currency,
  data,
  isLoading = false,
}: AdminRevenueActivityChartProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Revenue Activity</CardTitle>

        <CardDescription>
          Completed transaction revenue in {currency} across the selected
          period.
        </CardDescription>
      </CardHeader>

      <CardContent>
        {isLoading ? (
          <div className="h-80 w-full animate-pulse rounded-lg bg-muted" />
        ) : data.length === 0 ? (
          <div className="flex h-80 items-center justify-center text-center">
            <p className="text-sm text-muted-foreground">
              No revenue activity is available for this period.
            </p>
          </div>
        ) : (
          <div className="h-80 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart
                data={data}
                margin={{
                  top: 8,
                  right: 8,
                  left: 0,
                  bottom: 8,
                }}
              >
                <CartesianGrid strokeDasharray="3 3" />

                <XAxis
                  dataKey="date"
                  tickFormatter={formatDate}
                  minTickGap={24}
                />

                <YAxis
                  tickFormatter={(value) =>
                    formatCurrency(Number(value), currency)
                  }
                />

                <Tooltip
                  labelFormatter={(value) => formatDate(String(value))}
                  formatter={(value) => [
                    formatCurrency(Number(value), currency),
                    'Revenue',
                  ]}
                />

                <Line
                  type="monotone"
                  dataKey="amount"
                  name="Revenue"
                  stroke="currentColor"
                  strokeWidth={2}
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}
      </CardContent>
    </Card>
  )
}

export default AdminRevenueActivityChart
