import { AlertCircle, ArrowLeft, Loader2 } from 'lucide-react'
import { Link } from 'react-router-dom'

import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import PaymentHistoryTable from '@/features/billing/components/PaymentHistoryTable'
import { usePaymentTransactions } from '@/features/billing/hooks/use_billing'

function PaymentHistory() {
  const {
    data: transactions = [],
    isPending,
    isError,
  } = usePaymentTransactions()

  return (
    <div className="mx-auto w-full max-w-7xl space-y-6">
      <section>
        <Link
          to="/billing"
          className="inline-flex items-center gap-1.5 text-sm font-medium text-muted-foreground hover:text-foreground"
        >
          <ArrowLeft className="size-4" />
          Back to Billing
        </Link>

        <h2 className="mt-4 text-2xl font-semibold tracking-tight sm:text-3xl">
          Payment History
        </h2>

        <p className="mt-2 max-w-2xl text-muted-foreground">
          Review your subscription payment transactions and their current
          status.
        </p>
      </section>

      {isPending && (
        <Card>
          <CardContent className="flex min-h-56 items-center justify-center">
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Loader2 className="size-4 animate-spin" />
              Loading payment history...
            </div>
          </CardContent>
        </Card>
      )}

      {isError && (
        <Card>
          <CardHeader>
            <CardTitle>Unable to load payment history</CardTitle>

            <CardDescription>
              We couldn't retrieve your payment transactions.
            </CardDescription>
          </CardHeader>

          <CardContent>
            <div className="flex items-center gap-2 text-sm text-destructive">
              <AlertCircle className="size-4" />
              Please try again later.
            </div>
          </CardContent>
        </Card>
      )}

      {!isPending && !isError && (
        <PaymentHistoryTable transactions={transactions} />
      )}

      <div>
        <Link to="/billing">
          <Button type="button" variant="outline">
            <ArrowLeft />
            Back to Billing
          </Button>
        </Link>
      </div>
    </div>
  )
}

export default PaymentHistory
