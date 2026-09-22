import { CircleDollarSign } from 'lucide-react'

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import type { AdminRevenueMetrics } from '@/features/admin/types'

interface AdminRevenueSummaryProps {
  revenue: AdminRevenueMetrics | undefined
  isLoading: boolean
}

function formatRevenue(value: string, currency: string) {
  const amount = Number(value)

  if (!Number.isFinite(amount)) {
    return `${currency} ${value}`
  }

  return new Intl.NumberFormat(undefined, {
    style: 'currency',
    currency,
    maximumFractionDigits: 2,
  }).format(amount)
}

function AdminRevenueSummary({ revenue, isLoading }: AdminRevenueSummaryProps) {
  const currencies = Object.entries(revenue?.total_revenue_by_currency ?? {})

  return (
    <Card>
      <CardHeader>
        <div className="flex items-start gap-3">
          <div className="flex size-9 shrink-0 items-center justify-center rounded-lg bg-primary/10 text-primary">
            <CircleDollarSign className="size-5" />
          </div>

          <div>
            <CardTitle>Revenue Summary</CardTitle>

            <CardDescription className="mt-1">
              Completed transaction revenue grouped by currency.
            </CardDescription>
          </div>
        </div>
      </CardHeader>

      <CardContent>
        {isLoading ? (
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {Array.from({ length: 3 }).map((_, index) => (
              <div key={index} className="rounded-lg border p-4">
                <div className="h-4 w-16 animate-pulse rounded bg-muted" />

                <div className="mt-3 h-7 w-32 animate-pulse rounded bg-muted" />
              </div>
            ))}
          </div>
        ) : currencies.length === 0 ? (
          <div className="flex min-h-24 items-center justify-center text-center">
            <p className="text-sm text-muted-foreground">
              No completed transaction revenue is available.
            </p>
          </div>
        ) : (
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {currencies.map(([currency, value]) => (
              <div key={currency} className="rounded-lg border p-4">
                <p className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                  {currency}
                </p>

                <p className="mt-2 text-xl font-semibold tracking-tight">
                  {formatRevenue(value, currency)}
                </p>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  )
}

export default AdminRevenueSummary
