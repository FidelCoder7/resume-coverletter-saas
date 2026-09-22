import { Banknote, CreditCard, Receipt, WalletCards } from 'lucide-react'

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import AdminAnalyticsDistribution from '@/features/admin/components/analytics/AdminAnalyticsDistribution'
import AdminAnalyticsPeriodSelector, {
  type AdminAnalyticsPeriod,
} from '@/features/admin/components/analytics/AdminAnalyticsPeriodSelector'
import AdminMetricCard from '@/features/admin/components/dashboard/AdminMetricCard'
import AdminPaymentActivityChart from '@/features/admin/components/analytics/AdminPaymentActivityChart'
import AdminRevenueActivityChart from '@/features/admin/components/analytics/AdminRevenueActivityChart'
import type { AdminPaymentAnalyticsResponse } from '@/features/admin/types'

interface AdminPaymentAnalyticsProps {
  data: AdminPaymentAnalyticsResponse | undefined
  isLoading: boolean
  period: AdminAnalyticsPeriod
  onPeriodChange: (period: AdminAnalyticsPeriod) => void
}

const planLabels: Record<string, string> = {
  free: 'Free',
  pro: 'Pro',
}

const transactionTypeLabels: Record<string, string> = {
  subscription_purchase: 'Subscription Purchase',
  subscription_renewal: 'Subscription Renewal',
  subscription_upgrade: 'Subscription Upgrade',
  subscription_downgrade: 'Subscription Downgrade',
}

const providerLabels: Record<string, string> = {
  pesapal: 'PesaPal',
}

const paymentMethodLabels: Record<string, string> = {
  mpesa: 'M-Pesa',
  card: 'Card',
  bank: 'Bank',
  other: 'Other',
}

function formatLabel(value: string, labels: Record<string, string>): string {
  return labels[value] ?? value.replaceAll('_', ' ')
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

function AdminPaymentAnalytics({
  data,
  isLoading,
  period,
  onPeriodChange,
}: AdminPaymentAnalyticsProps) {
  const statusDistribution = [
    {
      key: 'completed',
      label: 'Completed',
      value: data?.completed_transactions ?? 0,
    },
    {
      key: 'pending',
      label: 'Pending',
      value: data?.pending_transactions ?? 0,
    },
    {
      key: 'failed',
      label: 'Failed',
      value: data?.failed_transactions ?? 0,
    },
    {
      key: 'cancelled',
      label: 'Cancelled',
      value: data?.cancelled_transactions ?? 0,
    },
    {
      key: 'expired',
      label: 'Expired',
      value: data?.expired_transactions ?? 0,
    },
  ]

  const planDistribution = Object.entries(data?.transactions_by_plan ?? {}).map(
    ([key, value]) => ({
      key,
      label: formatLabel(key, planLabels),
      value,
    }),
  )

  const transactionTypeDistribution = Object.entries(
    data?.transactions_by_type ?? {},
  ).map(([key, value]) => ({
    key,
    label: formatLabel(key, transactionTypeLabels),
    value,
  }))

  const providerDistribution = Object.entries(
    data?.transactions_by_provider ?? {},
  ).map(([key, value]) => ({
    key,
    label: formatLabel(key, providerLabels),
    value,
  }))

  const paymentMethodDistribution = Object.entries(
    data?.transactions_by_payment_method ?? {},
  ).map(([key, value]) => ({
    key,
    label: formatLabel(key, paymentMethodLabels),
    value,
  }))

  const revenueCurrencies = Object.keys(data?.revenue_activity ?? {}).sort()

  return (
    <div className="space-y-6">
      <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
        <div>
          <h2 className="text-lg font-semibold">Payment Analytics</h2>

          <p className="mt-1 text-sm text-muted-foreground">
            Payment transaction and revenue activity for the selected period.
          </p>
        </div>

        <AdminAnalyticsPeriodSelector
          value={period}
          onChange={onPeriodChange}
          disabled={isLoading}
        />
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <AdminMetricCard
          title="Transactions"
          value={data?.total_transactions ?? 0}
          description={`Transactions during the last ${period} days.`}
          icon={Receipt}
          isLoading={isLoading}
        />

        <AdminMetricCard
          title="Completed"
          value={data?.completed_transactions ?? 0}
          description="Successfully completed payment transactions."
          icon={CreditCard}
          isLoading={isLoading}
        />

        <AdminMetricCard
          title="Failed"
          value={data?.failed_transactions ?? 0}
          description="Payment transactions that failed."
          icon={Banknote}
          isLoading={isLoading}
        />
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Revenue Summary</CardTitle>
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
          ) : Object.keys(data?.total_revenue_by_currency ?? {}).length ===
            0 ? (
            <div className="flex min-h-24 items-center justify-center text-center">
              <p className="text-sm text-muted-foreground">
                No completed transaction revenue is available for this period.
              </p>
            </div>
          ) : (
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {Object.entries(data?.total_revenue_by_currency ?? {}).map(
                ([currency, value]) => (
                  <div key={currency} className="rounded-lg border p-4">
                    <p className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                      {currency}
                    </p>

                    <p className="mt-2 text-xl font-semibold tracking-tight">
                      {formatRevenue(value, currency)}
                    </p>
                  </div>
                ),
              )}
            </div>
          )}
        </CardContent>
      </Card>

      <div className="grid gap-6 lg:grid-cols-2">
        <AdminAnalyticsDistribution
          title="Transaction Status"
          description="Transactions grouped by their current payment status."
          items={statusDistribution}
          isLoading={isLoading}
        />

        <AdminAnalyticsDistribution
          title="Subscription Plan"
          description="Transactions grouped by subscription plan."
          items={planDistribution}
          isLoading={isLoading}
        />

        <AdminAnalyticsDistribution
          title="Transaction Type"
          description="Transactions grouped by transaction type."
          items={transactionTypeDistribution}
          isLoading={isLoading}
        />

        <AdminAnalyticsDistribution
          title="Payment Provider"
          description="Transactions grouped by payment provider."
          items={providerDistribution}
          isLoading={isLoading}
        />

        <AdminAnalyticsDistribution
          title="Payment Method"
          description="Transactions grouped by payment method."
          items={paymentMethodDistribution}
          isLoading={isLoading}
        />
      </div>

      <AdminPaymentActivityChart
        data={data?.transaction_activity ?? []}
        isLoading={isLoading}
      />

      {revenueCurrencies.map((currency) => (
        <AdminRevenueActivityChart
          key={currency}
          currency={currency}
          data={data?.revenue_activity[currency] ?? []}
          isLoading={isLoading}
        />
      ))}

      {!isLoading && revenueCurrencies.length === 0 && (
        <Card>
          <CardContent className="flex min-h-32 items-center justify-center text-center">
            <div>
              <WalletCards className="mx-auto size-8 text-muted-foreground" />

              <p className="mt-3 text-sm font-medium">No revenue activity</p>

              <p className="mt-1 text-sm text-muted-foreground">
                Revenue charts will appear when completed transactions are
                recorded.
              </p>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

export default AdminPaymentAnalytics
