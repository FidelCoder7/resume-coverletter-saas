import { AlertCircle, ArrowLeft, Loader2 } from 'lucide-react'
import { Link, useNavigate, useParams } from 'react-router-dom'

import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import PaymentTransactionDetails from '@/features/billing/components/PaymentTransactionDetails'
import {
  usePaymentTransaction,
  useSynchronizePaymentStatus,
} from '@/features/billing/hooks/use_billing'

function PaymentDetails() {
  const { transactionId = '' } = useParams<{ transactionId: string }>()
  const navigate = useNavigate()

  const {
    data: transaction,
    isPending,
    isError,
  } = usePaymentTransaction(transactionId)

  const synchronizeMutation = useSynchronizePaymentStatus()

  const handleSynchronize = () => {
    if (!transactionId) {
      return
    }

    synchronizeMutation.mutate(transactionId)
  }

  if (isPending) {
    return (
      <div className="mx-auto flex min-h-[60vh] w-full max-w-7xl items-center justify-center">
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <Loader2 className="size-4 animate-spin" />
          Loading payment details...
        </div>
      </div>
    )
  }

  if (isError || !transaction) {
    return (
      <div className="mx-auto flex min-h-[60vh] w-full max-w-lg items-center justify-center">
        <Card className="w-full">
          <CardHeader>
            <CardTitle>Payment not found</CardTitle>
          </CardHeader>

          <CardContent>
            <div className="flex items-start gap-2 text-sm text-muted-foreground">
              <AlertCircle className="mt-0.5 size-4 shrink-0" />
              <p>We couldn't retrieve the requested payment transaction.</p>
            </div>

            <Button
              type="button"
              variant="outline"
              className="mt-5"
              onClick={() => navigate('/billing/payments')}
            >
              <ArrowLeft />
              Back to Payment History
            </Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="mx-auto w-full max-w-7xl space-y-6">
      <section>
        <Link
          to="/billing/payments"
          className="inline-flex items-center gap-1.5 text-sm font-medium text-muted-foreground hover:text-foreground"
        >
          <ArrowLeft className="size-4" />
          Back to Payment History
        </Link>

        <h2 className="mt-4 text-2xl font-semibold tracking-tight sm:text-3xl">
          Payment Details
        </h2>

        <p className="mt-2 max-w-2xl text-muted-foreground">
          Review the status and details of this payment transaction.
        </p>
      </section>

      <PaymentTransactionDetails
        transaction={transaction}
        onSynchronize={handleSynchronize}
        isSynchronizing={synchronizeMutation.isPending}
      />
    </div>
  )
}

export default PaymentDetails
