import { ArrowRight, CreditCard, Receipt } from 'lucide-react'
import { Link } from 'react-router-dom'

import { buttonVariants } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import CurrentPlanCard from '@/features/billing/components/CurrentPlanCard'
import UsageDashboard from '@/features/billing/components/UsageDashboard'
import { useAuth } from '@/features/auth/hooks/use_auth'
import { cn } from '@/lib/utils'

function BillingDashboard() {
  const { user } = useAuth()

  const subscriptionPlan = user?.subscription_plan ?? 'free'

  return (
    <div className="mx-auto w-full max-w-7xl space-y-8">
      <section>
        <div className="flex items-start gap-3">
          <div className="flex size-10 shrink-0 items-center justify-center rounded-lg bg-primary/10 text-primary">
            <CreditCard className="size-5" />
          </div>

          <div>
            <p className="text-sm font-medium text-primary">Subscription</p>

            <h2 className="mt-1 text-2xl font-semibold tracking-tight sm:text-3xl">
              Billing
            </h2>

            <p className="mt-2 max-w-2xl text-muted-foreground">
              Manage your subscription and monitor your AI feature usage.
            </p>
          </div>
        </div>
      </section>

      <CurrentPlanCard plan={subscriptionPlan} />

      <UsageDashboard />

      <Card>
        <CardHeader>
          <CardTitle>Payment History</CardTitle>
        </CardHeader>

        <CardContent>
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div className="flex items-start gap-3">
              <div className="flex size-9 shrink-0 items-center justify-center rounded-lg bg-muted text-muted-foreground">
                <Receipt className="size-5" />
              </div>

              <div>
                <p className="text-sm font-medium">
                  View your subscription payments
                </p>

                <p className="mt-1 text-sm text-muted-foreground">
                  Review payment amounts, methods, transaction IDs, and current
                  payment status.
                </p>
              </div>
            </div>

            <Link
              to="/billing/payments"
              className={cn(buttonVariants({ variant: 'outline' }), 'shrink-0')}
            >
              Payment history
              <ArrowRight />
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default BillingDashboard
