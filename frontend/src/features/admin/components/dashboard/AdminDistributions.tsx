import {
  Activity,
  CheckCircle2,
  CircleDollarSign,
  ShieldCheck,
  UserCheck,
  UserX,
  XCircle,
} from 'lucide-react'

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import type { AdminDashboardMetricsResponse } from '@/features/admin/types'

interface AdminDistributionsProps {
  metrics: AdminDashboardMetricsResponse | undefined
  isLoading: boolean
}

interface DistributionItem {
  label: string
  value: number
  icon: typeof Activity
}

interface DistributionListProps {
  items: DistributionItem[]
  isLoading: boolean
  valueLabel: string
  emptyMessage: string
}

function DistributionList({
  items,
  isLoading,
  valueLabel,
  emptyMessage,
}: DistributionListProps) {
  if (isLoading) {
    return (
      <div className="space-y-4">
        {Array.from({ length: 4 }).map((_, index) => (
          <div key={index} className="flex items-center gap-3">
            <div className="size-8 animate-pulse rounded-lg bg-muted" />

            <div className="min-w-0 flex-1">
              <div className="h-4 w-28 animate-pulse rounded bg-muted" />

              <div className="mt-2 h-3 w-16 animate-pulse rounded bg-muted" />
            </div>

            <div className="h-5 w-10 animate-pulse rounded bg-muted" />
          </div>
        ))}
      </div>
    )
  }

  if (items.every((item) => item.value === 0)) {
    return (
      <div className="flex min-h-32 items-center justify-center text-center">
        <p className="text-sm text-muted-foreground">{emptyMessage}</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {items.map((item) => {
        const Icon = item.icon

        return (
          <div key={item.label} className="flex items-center gap-3">
            <div className="flex size-8 shrink-0 items-center justify-center rounded-lg bg-muted text-muted-foreground">
              <Icon className="size-4" />
            </div>

            <div className="min-w-0 flex-1">
              <p className="truncate text-sm font-medium">{item.label}</p>

              <p className="text-xs text-muted-foreground">
                {item.value.toLocaleString()} {valueLabel}
              </p>
            </div>

            <p className="text-sm font-semibold">
              {item.value.toLocaleString()}
            </p>
          </div>
        )
      })}
    </div>
  )
}

function AdminDistributions({ metrics, isLoading }: AdminDistributionsProps) {
  const users = metrics?.users

  const subscriptionItems: DistributionItem[] = [
    {
      label: 'Free',
      value: metrics?.subscriptions.free_users ?? 0,
      icon: Activity,
    },
    {
      label: 'Pro',
      value: metrics?.subscriptions.pro_users ?? 0,
      icon: ShieldCheck,
    },
    {
      label: 'Active subscriptions',
      value: metrics?.subscriptions.active_subscriptions ?? 0,
      icon: CheckCircle2,
    },
  ]

  const userStatusItems: DistributionItem[] = [
    {
      label: 'Active',
      value: users?.active_users ?? 0,
      icon: UserCheck,
    },
    {
      label: 'Suspended',
      value: users?.suspended_users ?? 0,
      icon: UserX,
    },
    {
      label: 'Deleted',
      value: users?.deleted_users ?? 0,
      icon: XCircle,
    },
    {
      label: 'Administrators',
      value: users?.total_admins ?? 0,
      icon: ShieldCheck,
    },
  ]

  const paymentItems: DistributionItem[] = [
    {
      label: 'Completed',
      value: metrics?.revenue.completed_transactions ?? 0,
      icon: CheckCircle2,
    },
    {
      label: 'Pending',
      value: metrics?.revenue.pending_transactions ?? 0,
      icon: Activity,
    },
    {
      label: 'Failed',
      value: metrics?.revenue.failed_transactions ?? 0,
      icon: XCircle,
    },
    {
      label: 'Cancelled',
      value: metrics?.revenue.cancelled_transactions ?? 0,
      icon: CircleDollarSign,
    },
    {
      label: 'Expired',
      value: metrics?.revenue.expired_transactions ?? 0,
      icon: XCircle,
    },
  ]

  return (
    <section className="grid gap-4 lg:grid-cols-3">
      <Card>
        <CardHeader>
          <CardTitle>Subscriptions</CardTitle>

          <CardDescription>
            Current subscription distribution across users.
          </CardDescription>
        </CardHeader>

        <CardContent>
          <DistributionList
            items={subscriptionItems}
            isLoading={isLoading}
            valueLabel="users"
            emptyMessage="No subscription data available."
          />
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>User Status</CardTitle>

          <CardDescription>
            Current account status across the platform.
          </CardDescription>
        </CardHeader>

        <CardContent>
          <DistributionList
            items={userStatusItems}
            isLoading={isLoading}
            valueLabel="users"
            emptyMessage="No user status data available."
          />
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Payment Status</CardTitle>

          <CardDescription>
            Payment transaction counts by current status.
          </CardDescription>
        </CardHeader>

        <CardContent>
          <DistributionList
            items={paymentItems}
            isLoading={isLoading}
            valueLabel="transactions"
            emptyMessage="No payment transaction data available."
          />
        </CardContent>
      </Card>
    </section>
  )
}

export default AdminDistributions
