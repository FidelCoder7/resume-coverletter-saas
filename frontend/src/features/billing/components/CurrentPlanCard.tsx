import { Check, Sparkles } from 'lucide-react'
import { Link } from 'react-router-dom'

import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import type { SubscriptionPlan } from '@/types/user'

interface CurrentPlanCardProps {
  plan: SubscriptionPlan
}

const planDetails: Record<
  SubscriptionPlan,
  {
    label: string
    description: string
    features: string[]
  }
> = {
  free: {
    label: 'Free',
    description:
      'Your current plan gives you access to the core resume and AI workspace features.',
    features: [
      'Resume management',
      'AI-powered workspace',
      'Usage limits based on your plan',
    ],
  },
  pro: {
    label: 'Pro',
    description:
      'You are currently using the Pro plan with expanded access to AI-powered features.',
    features: [
      'Resume management',
      'AI-powered workspace',
      'Expanded AI usage limits',
    ],
  },
}

function CurrentPlanCard({ plan }: CurrentPlanCardProps) {
  const details = planDetails[plan]

  return (
    <Card>
      <CardHeader>
        <div className="flex items-start justify-between gap-4">
          <div>
            <CardTitle className="flex items-center gap-2">
              <Sparkles className="size-5 text-primary" />
              Current Plan
            </CardTitle>

            <CardDescription className="mt-1">
              Your active subscription plan.
            </CardDescription>
          </div>

          <span className="rounded-full bg-primary/10 px-3 py-1 text-xs font-medium capitalize text-primary">
            {details.label}
          </span>
        </div>
      </CardHeader>

      <CardContent>
        <div className="space-y-5">
          <div>
            <p className="text-2xl font-semibold">{details.label}</p>

            <p className="mt-1 max-w-2xl text-sm text-muted-foreground">
              {details.description}
            </p>
          </div>

          <ul className="grid gap-2 sm:grid-cols-3">
            {details.features.map((feature) => (
              <li
                key={feature}
                className="flex items-start gap-2 text-sm text-muted-foreground"
              >
                <Check className="mt-0.5 size-4 shrink-0 text-primary" />
                <span>{feature}</span>
              </li>
            ))}
          </ul>

          {plan === 'free' && (
            <div className="flex flex-wrap items-center gap-3 border-t pt-5">
              <Link to="/billing/upgrade">
                <Button type="button">Upgrade to Pro</Button>
              </Link>

              <p className="text-xs text-muted-foreground">
                View your current usage below before upgrading.
              </p>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  )
}

export default CurrentPlanCard
