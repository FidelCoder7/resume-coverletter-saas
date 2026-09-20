import { AlertCircle, CheckCircle2, Clock3, RefreshCw } from 'lucide-react'

import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import PaymentStatusBadge from '@/features/billing/components/PaymentStatusBadge'
import type { PaymentTransaction } from '@/features/billing/types'

interface PaymentTransactionDetailsProps {
  transaction: PaymentTransaction
  onSynchronize: () => void
  isSynchronizing: boolean
}

const transactionTypeLabels: Record<
  PaymentTransaction['transaction_type'],
  string
> = {
  subscription_purchase: 'Subscription Purchase',
  subscription_renewal: 'Subscription Renewal',
  subscription_upgrade: 'Subscription Upgrade',
  subscription_downgrade: 'Subscription Downgrade',
}

const paymentMethodLabels: Record<
  NonNullable<PaymentTransaction['payment_method']>,
  string
> = {
  mpesa: 'M-Pesa',
  card: 'Card',
  bank: 'Bank',
  other: 'Other',
}

const statusIcons: Record<PaymentTransaction['status'], typeof Clock3> = {
  pending: Clock3,
  completed: CheckCircle2,
  failed: AlertCircle,
  cancelled: AlertCircle,
  expired: AlertCircle,
}

function PaymentTransactionDetails({
  transaction,
  onSynchronize,
  isSynchronizing,
}: PaymentTransactionDetailsProps) {
  const StatusIcon = statusIcons[transaction.status]

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div>
              <CardTitle>Payment Status</CardTitle>

              <CardDescription className="mt-1">
                Current status reported by the payment provider.
              </CardDescription>
            </div>

            <PaymentStatusBadge status={transaction.status} />
          </div>
        </CardHeader>

        <CardContent>
          <div className="flex items-start gap-3 rounded-lg bg-muted/50 p-4">
            <StatusIcon className="mt-0.5 size-5 shrink-0" />

            <div>
              <p className="text-sm font-medium capitalize">
                Payment {transaction.status}
              </p>

              <p className="mt-1 text-sm text-muted-foreground">
                {transaction.status === 'pending' &&
                  'This payment is still being processed.'}

                {transaction.status === 'completed' &&
                  'This payment has been completed successfully.'}

                {transaction.status === 'failed' &&
                  'The payment could not be completed.'}

                {transaction.status === 'cancelled' &&
                  'This payment was cancelled.'}

                {transaction.status === 'expired' &&
                  'This payment has expired.'}
              </p>
            </div>
          </div>

          {transaction.failure_reason && (
            <div className="mt-4 rounded-lg border border-destructive/20 bg-destructive/5 p-4">
              <p className="text-sm font-medium text-destructive">
                Failure reason
              </p>

              <p className="mt-1 text-sm text-muted-foreground">
                {transaction.failure_reason}
              </p>
            </div>
          )}

          <div className="mt-5">
            <Button
              type="button"
              variant="outline"
              onClick={onSynchronize}
              disabled={isSynchronizing}
            >
              <RefreshCw
                className={isSynchronizing ? 'animate-spin' : undefined}
              />
              {isSynchronizing ? 'Checking status...' : 'Check payment status'}
            </Button>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Transaction Details</CardTitle>

          <CardDescription>
            Information associated with this payment transaction.
          </CardDescription>
        </CardHeader>

        <CardContent>
          <dl className="grid gap-5 sm:grid-cols-2">
            <div>
              <dt className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                Transaction ID
              </dt>

              <dd className="mt-1 break-all text-sm font-medium">
                {transaction.id}
              </dd>
            </div>

            <div>
              <dt className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                Provider
              </dt>

              <dd className="mt-1 text-sm font-medium uppercase">
                {transaction.provider}
              </dd>
            </div>

            <div>
              <dt className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                Provider Order ID
              </dt>

              <dd className="mt-1 break-all text-sm font-medium">
                {transaction.provider_order_id}
              </dd>
            </div>

            <div>
              <dt className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                Provider Transaction ID
              </dt>

              <dd className="mt-1 break-all text-sm font-medium">
                {transaction.provider_transaction_id ?? 'Not available'}
              </dd>
            </div>

            <div>
              <dt className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                Transaction Type
              </dt>

              <dd className="mt-1 text-sm font-medium">
                {transactionTypeLabels[transaction.transaction_type]}
              </dd>
            </div>

            <div>
              <dt className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                Subscription Plan
              </dt>

              <dd className="mt-1 capitalize text-sm font-medium">
                {transaction.subscription_plan}
              </dd>
            </div>

            <div>
              <dt className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                Amount
              </dt>

              <dd className="mt-1 text-sm font-medium">
                {transaction.currency} {transaction.amount}
              </dd>
            </div>

            <div>
              <dt className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                Payment Method
              </dt>

              <dd className="mt-1 text-sm font-medium">
                {transaction.payment_method
                  ? paymentMethodLabels[transaction.payment_method]
                  : 'Not specified'}
              </dd>
            </div>
          </dl>
        </CardContent>
      </Card>
    </div>
  )
}

export default PaymentTransactionDetails
