import { FileText, Mail, RefreshCw, Target } from 'lucide-react'

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import type { FeatureUsage } from '@/features/billing/types'

interface UsageFeatureCardProps {
  usage: FeatureUsage
}

const featureDetails = {
  resume_generation: {
    label: 'Resume Generation',
    description: 'AI-generated resumes during the current billing period.',
    icon: FileText,
  },
  cover_letter_generation: {
    label: 'Cover Letter Generation',
    description:
      'AI-generated cover letters during the current billing period.',
    icon: Mail,
  },
  cover_letter_regeneration: {
    label: 'Cover Letter Regeneration',
    description:
      'AI cover letter regenerations during the current billing period.',
    icon: RefreshCw,
  },
  ats_optimization: {
    label: 'ATS Optimization',
    description: 'ATS optimization requests during the current billing period.',
    icon: Target,
  },
} as const

function UsageFeatureCard({ usage }: UsageFeatureCardProps) {
  const details = featureDetails[usage.feature]
  const Icon = details.icon

  const percentage =
    usage.limit_value > 0
      ? Math.min((usage.usage / usage.limit_value) * 100, 100)
      : 0

  const remaining = Math.max(usage.remaining, 0)

  return (
    <Card>
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between gap-4">
          <div className="flex items-start gap-3">
            <div className="flex size-9 shrink-0 items-center justify-center rounded-lg bg-primary/10 text-primary">
              <Icon className="size-5" />
            </div>

            <div>
              <CardTitle className="text-sm font-medium">
                {details.label}
              </CardTitle>

              <p className="mt-1 text-xs text-muted-foreground">
                {details.description}
              </p>
            </div>
          </div>

          <span className="shrink-0 text-sm font-medium">
            {usage.usage} / {usage.limit_value}
          </span>
        </div>
      </CardHeader>

      <CardContent>
        <div
          className="h-2 overflow-hidden rounded-full bg-muted"
          role="progressbar"
          aria-label={`${details.label} usage`}
          aria-valuemin={0}
          aria-valuemax={usage.limit_value}
          aria-valuenow={Math.min(usage.usage, usage.limit_value)}
        >
          <div
            className="h-full rounded-full bg-primary transition-all"
            style={{ width: `${percentage}%` }}
          />
        </div>

        <div className="mt-2 flex items-center justify-between text-xs text-muted-foreground">
          <span>{remaining} remaining</span>

          <span className="capitalize">{usage.period}</span>
        </div>
      </CardContent>
    </Card>
  )
}

export default UsageFeatureCard
