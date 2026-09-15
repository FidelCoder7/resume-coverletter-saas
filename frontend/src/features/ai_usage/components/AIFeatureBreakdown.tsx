import { FileText, Mail, RefreshCw, SearchCheck } from 'lucide-react'

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import type { AIFeature, AIFeatureUsage } from '@/features/ai_usage/types'

interface AIFeatureBreakdownProps {
  features: AIFeatureUsage[]
}

const featureConfig: Record<
  AIFeature,
  {
    label: string
    icon: typeof FileText
  }
> = {
  resume_generation: {
    label: 'Resume Generation',
    icon: FileText,
  },

  cover_letter_generation: {
    label: 'Cover Letter Generation',
    icon: Mail,
  },

  cover_letter_regeneration: {
    label: 'Cover Letter Regeneration',
    icon: RefreshCw,
  },

  ats_optimization: {
    label: 'ATS Optimization',
    icon: SearchCheck,
  },
}

function AIFeatureBreakdown({ features }: AIFeatureBreakdownProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Usage by Feature</CardTitle>

        <CardDescription>
          AI request and token usage grouped by feature.
        </CardDescription>
      </CardHeader>

      <CardContent>
        {features.length === 0 ? (
          <div className="flex flex-col items-center justify-center rounded-lg border border-dashed px-6 py-10 text-center">
            <FileText className="size-7 text-muted-foreground" />

            <p className="mt-3 text-sm text-muted-foreground">
              No AI feature usage was recorded for this period.
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {features.map((feature) => {
              const config = featureConfig[feature.feature]
              const Icon = config.icon

              return (
                <div
                  key={feature.feature}
                  className="flex items-center justify-between gap-4 rounded-lg border p-4"
                >
                  <div className="flex min-w-0 items-center gap-3">
                    <div className="flex size-9 shrink-0 items-center justify-center rounded-lg bg-muted">
                      <Icon className="size-4 text-muted-foreground" />
                    </div>

                    <div className="min-w-0">
                      <p className="truncate text-sm font-medium">
                        {config.label}
                      </p>

                      <p className="mt-1 text-xs text-muted-foreground">
                        {feature.requests.toLocaleString()} request
                        {feature.requests === 1 ? '' : 's'}
                      </p>
                    </div>
                  </div>

                  <div className="shrink-0 text-right">
                    <p className="text-sm font-medium">
                      {feature.total_tokens.toLocaleString()}
                    </p>

                    <p className="text-xs text-muted-foreground">tokens</p>
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </CardContent>
    </Card>
  )
}

export default AIFeatureBreakdown
