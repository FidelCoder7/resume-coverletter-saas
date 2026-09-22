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
import type { AdminTimeSeriesPoint } from '@/features/admin/types'

interface AdminAuditActivityChartProps {
  data: AdminTimeSeriesPoint[] | undefined
  isLoading: boolean
  isError: boolean
}

function formatDate(value: string) {
  const date = new Date(`${value}T00:00:00`)

  if (Number.isNaN(date.getTime())) {
    return value
  }

  return new Intl.DateTimeFormat(undefined, {
    month: 'short',
    day: 'numeric',
  }).format(date)
}

function AdminAuditActivityChart({
  data,
  isLoading,
  isError,
}: AdminAuditActivityChartProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Administrative Activity</CardTitle>

        <CardDescription>
          Daily administrative audit activity during the selected period.
        </CardDescription>
      </CardHeader>

      <CardContent>
        {isLoading ? (
          <div
            className="h-72 animate-pulse rounded-lg bg-muted"
            aria-label="Loading administrative activity chart"
          />
        ) : isError ? (
          <div className="flex h-72 items-center justify-center text-center">
            <div>
              <p className="text-sm font-medium">
                Unable to load audit activity
              </p>

              <p className="mt-1 text-sm text-muted-foreground">
                The historical audit activity could not be retrieved.
              </p>
            </div>
          </div>
        ) : !data?.length ? (
          <div className="flex h-72 items-center justify-center text-center">
            <div>
              <p className="text-sm font-medium">No audit activity</p>

              <p className="mt-1 text-sm text-muted-foreground">
                There is no audit activity for the selected period.
              </p>
            </div>
          </div>
        ) : (
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart
                data={data}
                margin={{
                  top: 8,
                  right: 8,
                  left: -16,
                  bottom: 8,
                }}
              >
                <CartesianGrid
                  strokeDasharray="3 3"
                  className="stroke-border"
                />

                <XAxis
                  dataKey="date"
                  tickFormatter={formatDate}
                  tickLine={false}
                  axisLine={false}
                  minTickGap={24}
                  className="text-xs"
                />

                <YAxis
                  allowDecimals={false}
                  tickLine={false}
                  axisLine={false}
                  width={40}
                  className="text-xs"
                />

                <Tooltip
                  labelFormatter={(value) => formatDate(String(value))}
                  formatter={(value) => [
                    Number(value).toLocaleString(),
                    'Audit events',
                  ]}
                  contentStyle={{
                    borderRadius: '0.75rem',
                    border: '1px solid hsl(var(--border))',
                    backgroundColor: 'hsl(var(--background))',
                  }}
                />

                <Line
                  type="monotone"
                  dataKey="count"
                  name="Audit events"
                  stroke="currentColor"
                  className="text-primary"
                  strokeWidth={2}
                  dot={false}
                  activeDot={{ r: 4 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}
      </CardContent>
    </Card>
  )
}

export default AdminAuditActivityChart
