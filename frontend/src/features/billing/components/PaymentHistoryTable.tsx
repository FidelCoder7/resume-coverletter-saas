import { Eye, Receipt } from 'lucide-react'
import { Link } from 'react-router-dom'

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import PaymentStatusBadge from '@/features/billing/components/PaymentStatusBadge'
import type { PaymentTransaction } from '@/features/billing/types'

interface PaymentHistoryTableProps {
  transactions: PaymentTransaction[]
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

function formatAmount(transaction: PaymentTransaction) {
  return `${transaction.currency} ${transaction.amount}`
}

function PaymentHistoryTable({ transactions }: PaymentHistoryTableProps) {
  if (transactions.length === 0) {
    return (
      <Card>
        <CardContent className="flex min-h-56 flex-col items-center justify-center text-center">
          <Receipt className="size-9 text-muted-foreground" />

          <h3 className="mt-3 text-sm font-semibold">
            No payment transactions
          </h3>

          <p className="mt-1 max-w-md text-sm text-muted-foreground">
            Your payment transactions will appear here after you make a
            subscription payment.
          </p>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Payment History</CardTitle>

        <CardDescription>
          View your subscription payment transactions and their current status.
        </CardDescription>
      </CardHeader>

      <CardContent>
        <div className="overflow-x-auto">
          <table className="w-full min-w-[760px] text-sm">
            <thead>
              <tr className="border-b text-left text-xs text-muted-foreground">
                <th className="px-3 py-3 font-medium">Transaction</th>
                <th className="px-3 py-3 font-medium">Type</th>
                <th className="px-3 py-3 font-medium">Plan</th>
                <th className="px-3 py-3 font-medium">Amount</th>
                <th className="px-3 py-3 font-medium">Method</th>
                <th className="px-3 py-3 font-medium">Status</th>
                <th className="px-3 py-3 text-right font-medium">Action</th>
              </tr>
            </thead>

            <tbody className="divide-y">
              {transactions.map((transaction) => (
                <tr
                  key={transaction.id}
                  className="transition-colors hover:bg-muted/50"
                >
                  <td className="px-3 py-4">
                    <div className="max-w-[180px]">
                      <p className="truncate font-medium">{transaction.id}</p>

                      <p className="mt-1 truncate text-xs text-muted-foreground">
                        Order: {transaction.provider_order_id}
                      </p>
                    </div>
                  </td>

                  <td className="px-3 py-4">
                    {transactionTypeLabels[transaction.transaction_type]}
                  </td>

                  <td className="px-3 py-4 capitalize">
                    {transaction.subscription_plan}
                  </td>

                  <td className="px-3 py-4 font-medium">
                    {formatAmount(transaction)}
                  </td>

                  <td className="px-3 py-4">
                    {transaction.payment_method
                      ? paymentMethodLabels[transaction.payment_method]
                      : 'Not specified'}
                  </td>

                  <td className="px-3 py-4">
                    <PaymentStatusBadge status={transaction.status} />
                  </td>

                  <td className="px-3 py-4 text-right">
                    <Link
                      to={`/billing/payments/${transaction.id}`}
                      className="inline-flex items-center gap-1.5 text-sm font-medium text-primary hover:underline"
                    >
                      <Eye className="size-4" />
                      View
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </CardContent>
    </Card>
  )
}

export default PaymentHistoryTable
