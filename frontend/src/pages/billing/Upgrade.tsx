import {
  ArrowLeft,
  Check,
  CreditCard,
  Landmark,
  Loader2,
  Smartphone,
} from 'lucide-react'
import { Link } from 'react-router-dom'
import { useState } from 'react'

import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { useInitiatePayment } from '@/features/billing/hooks/use_billing'
import type { PaymentMethod } from '@/features/billing/types'
import { useAuth } from '@/features/auth/hooks/use_auth'

interface PaymentMethodOption {
  value: PaymentMethod
  label: string
  description: string
  icon: typeof Smartphone
}

const paymentMethods: PaymentMethodOption[] = [
  {
    value: 'mpesa',
    label: 'M-Pesa',
    description: 'Pay using M-Pesa through PesaPal.',
    icon: Smartphone,
  },
  {
    value: 'card',
    label: 'Card',
    description: 'Pay using a supported debit or credit card.',
    icon: CreditCard,
  },
  {
    value: 'bank',
    label: 'Bank',
    description: 'Pay using a supported bank payment method.',
    icon: Landmark,
  },
]

const proFeatures = [
  'Expanded AI feature usage limits',
  'AI resume generation',
  'AI cover letter generation and regeneration',
  'ATS optimization',
  'Resume versioning and export',
]

function Upgrade() {
  const { user } = useAuth()
  const initiatePaymentMutation = useInitiatePayment()

  const [paymentMethod, setPaymentMethod] = useState<PaymentMethod>('mpesa')

  const isPro = user?.subscription_plan === 'pro'

  const handleUpgrade = () => {
    initiatePaymentMutation.mutate(
      {
        subscription_plan: 'pro',
        transaction_type: 'subscription_purchase',
        payment_method: paymentMethod,
      },
      {
        onSuccess: (response) => {
          if (!response.redirect_url) {
            return
          }

          window.location.assign(response.redirect_url)
        },
      },
    )
  }

  if (isPro) {
    return (
      <div className="mx-auto w-full max-w-3xl">
        <Card>
          <CardHeader>
            <CardTitle>You are already on Pro</CardTitle>
            <CardDescription>
              Your account already has an active Pro subscription.
            </CardDescription>
          </CardHeader>

          <CardContent>
            <div className="flex flex-wrap gap-3">
              <Link to="/billing">
                <Button type="button">
                  <ArrowLeft />
                  Back to Billing
                </Button>
              </Link>

              <Link to="/billing/usage">
                <Button type="button" variant="outline">
                  View Usage
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="mx-auto w-full max-w-5xl space-y-8">
      <section>
        <Link
          to="/billing"
          className="inline-flex items-center gap-1.5 text-sm font-medium text-muted-foreground hover:text-foreground"
        >
          <ArrowLeft className="size-4" />
          Back to Billing
        </Link>

        <div className="mt-5">
          <p className="text-sm font-medium text-primary">
            Subscription Upgrade
          </p>

          <h2 className="mt-1 text-2xl font-semibold tracking-tight sm:text-3xl">
            Upgrade to Pro
          </h2>

          <p className="mt-2 max-w-2xl text-muted-foreground">
            Unlock expanded access to the AI-powered features in your workspace.
          </p>
        </div>
      </section>

      <div className="grid gap-6 lg:grid-cols-[1fr_1.1fr]">
        <Card>
          <CardHeader>
            <CardTitle>Pro includes</CardTitle>
            <CardDescription>
              Your Pro subscription provides expanded access to the
              application's AI capabilities.
            </CardDescription>
          </CardHeader>

          <CardContent>
            <ul className="space-y-3">
              {proFeatures.map((feature) => (
                <li key={feature} className="flex items-start gap-2.5 text-sm">
                  <Check className="mt-0.5 size-4 shrink-0 text-primary" />
                  <span>{feature}</span>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Choose a payment method</CardTitle>
            <CardDescription>
              Your payment will be securely processed through PesaPal.
            </CardDescription>
          </CardHeader>

          <CardContent className="space-y-5">
            <div className="grid gap-3">
              {paymentMethods.map((method) => {
                const Icon = method.icon
                const selected = paymentMethod === method.value

                return (
                  <button
                    key={method.value}
                    type="button"
                    onClick={() => setPaymentMethod(method.value)}
                    className={`flex w-full items-start gap-3 rounded-lg border p-4 text-left transition-colors ${
                      selected
                        ? 'border-primary bg-primary/5'
                        : 'border-border hover:bg-muted/50'
                    }`}
                    aria-pressed={selected}
                  >
                    <div
                      className={`flex size-9 shrink-0 items-center justify-center rounded-lg ${
                        selected
                          ? 'bg-primary/10 text-primary'
                          : 'bg-muted text-muted-foreground'
                      }`}
                    >
                      <Icon className="size-5" />
                    </div>

                    <div className="min-w-0">
                      <p className="text-sm font-medium">{method.label}</p>
                      <p className="mt-1 text-xs text-muted-foreground">
                        {method.description}
                      </p>
                    </div>

                    <span
                      className={`ml-auto mt-1 size-4 shrink-0 rounded-full border ${
                        selected
                          ? 'border-primary bg-primary ring-4 ring-primary/10'
                          : 'border-muted-foreground/40'
                      }`}
                    />
                  </button>
                )
              })}
            </div>

            {initiatePaymentMutation.isError && (
              <div
                role="alert"
                className="rounded-lg border border-destructive/20 bg-destructive/5 p-4"
              >
                <p className="text-sm font-medium text-destructive">
                  Unable to start payment
                </p>

                <p className="mt-1 text-sm text-muted-foreground">
                  We couldn't initiate the payment. Please try again.
                </p>
              </div>
            )}

            {initiatePaymentMutation.isSuccess &&
              !initiatePaymentMutation.data.redirect_url && (
                <div
                  role="alert"
                  className="rounded-lg border border-destructive/20 bg-destructive/5 p-4"
                >
                  <p className="text-sm font-medium text-destructive">
                    Checkout unavailable
                  </p>

                  <p className="mt-1 text-sm text-muted-foreground">
                    The payment was created, but no checkout URL was returned.
                    Please check the payment history for its status.
                  </p>

                  <Link
                    to={`/billing/payments/${initiatePaymentMutation.data.transaction.id}`}
                    className="mt-3 inline-flex text-sm font-medium text-primary hover:underline"
                  >
                    View payment details
                  </Link>
                </div>
              )}

            <div className="border-t pt-5">
              <Button
                type="button"
                className="w-full"
                size="lg"
                onClick={handleUpgrade}
                disabled={initiatePaymentMutation.isPending}
              >
                {initiatePaymentMutation.isPending ? (
                  <>
                    <Loader2 className="animate-spin" />
                    Starting checkout...
                  </>
                ) : (
                  <>
                    Continue to PesaPal
                    <CreditCard />
                  </>
                )}
              </Button>

              <p className="mt-3 text-center text-xs text-muted-foreground">
                You will be redirected to PesaPal to complete your payment.
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default Upgrade
