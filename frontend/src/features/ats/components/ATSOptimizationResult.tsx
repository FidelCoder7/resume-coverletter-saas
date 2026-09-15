import {
  CheckCircle2,
  ClipboardCheck,
  Copy,
  FileText,
  Lightbulb,
  Search,
  XCircle,
} from 'lucide-react'
import { useState } from 'react'

import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import type { ATSOptimizationResponse } from '@/features/ats/types'

interface ATSOptimizationResultProps {
  result: ATSOptimizationResponse
}

function ATSOptimizationResult({ result }: ATSOptimizationResultProps) {
  const [copied, setCopied] = useState(false)

  async function handleCopy() {
    if (!result.optimized_resume) {
      return
    }

    await navigator.clipboard.writeText(result.optimized_resume)

    setCopied(true)

    window.setTimeout(() => {
      setCopied(false)
    }, 2000)
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
            <div>
              <div className="flex items-center gap-2">
                <ClipboardCheck className="size-5 text-primary" />

                <CardTitle>ATS Analysis</CardTitle>
              </div>

              <CardDescription className="mt-1">
                Analysis results for your selected resume and target job.
              </CardDescription>
            </div>

            <div className="flex items-center gap-2 rounded-lg border px-4 py-2">
              <span className="text-sm text-muted-foreground">ATS Score</span>

              <span className="text-2xl font-semibold">{result.ats_score}</span>
            </div>
          </div>
        </CardHeader>

        <CardContent>
          <div className="grid gap-4 md:grid-cols-3">
            <MetricCard
              icon={CheckCircle2}
              label="Matched Keywords"
              value={result.matched_keywords.length}
            />

            <MetricCard
              icon={XCircle}
              label="Missing Keywords"
              value={result.missing_keywords.length}
            />

            <MetricCard
              icon={Lightbulb}
              label="Recommendations"
              value={result.recommendations.length}
            />
          </div>
        </CardContent>
      </Card>

      <div className="grid gap-6 lg:grid-cols-2">
        <KeywordCard
          icon={CheckCircle2}
          title="Matched Keywords"
          description="Keywords already represented in your resume."
          items={result.matched_keywords}
          emptyMessage="No matching keywords were identified."
        />

        <KeywordCard
          icon={XCircle}
          title="Missing Keywords"
          description="Important terms from the job description that may be missing."
          items={result.missing_keywords}
          emptyMessage="No missing keywords were identified."
        />
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Recommendations</CardTitle>

          <CardDescription>
            Suggested improvements based on the ATS analysis.
          </CardDescription>
        </CardHeader>

        <CardContent>
          {result.recommendations.length > 0 ? (
            <ul className="space-y-3">
              {result.recommendations.map((recommendation, index) => (
                <li
                  key={`${recommendation}-${index}`}
                  className="flex gap-3 rounded-lg border p-4"
                >
                  <Lightbulb className="mt-0.5 size-5 shrink-0 text-primary" />

                  <p className="text-sm leading-6">{recommendation}</p>
                </li>
              ))}
            </ul>
          ) : (
            <EmptyState
              icon={Lightbulb}
              message="No additional recommendations were returned."
            />
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
            <div>
              <CardTitle>Optimized Resume</CardTitle>

              <CardDescription>
                AI-generated resume content optimized against the target job.
              </CardDescription>
            </div>

            {result.optimized_resume && (
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={handleCopy}
              >
                <Copy />

                {copied ? 'Copied' : 'Copy'}
              </Button>
            )}
          </div>
        </CardHeader>

        <CardContent>
          {result.optimized_resume ? (
            <div className="rounded-lg border bg-muted/20 p-6">
              <p className="whitespace-pre-wrap text-sm leading-7">
                {result.optimized_resume}
              </p>
            </div>
          ) : (
            <EmptyState
              icon={FileText}
              message="No optimized resume content was returned."
            />
          )}
        </CardContent>
      </Card>
    </div>
  )
}

interface MetricCardProps {
  icon: typeof CheckCircle2
  label: string
  value: number
}

function MetricCard({ icon: Icon, label, value }: MetricCardProps) {
  return (
    <div className="rounded-lg border p-4">
      <div className="flex items-center gap-2 text-sm text-muted-foreground">
        <Icon className="size-4" />

        <span>{label}</span>
      </div>

      <p className="mt-2 text-2xl font-semibold">{value}</p>
    </div>
  )
}

interface KeywordCardProps {
  icon: typeof CheckCircle2
  title: string
  description: string
  items: string[]
  emptyMessage: string
}

function KeywordCard({
  icon: Icon,
  title,
  description,
  items,
  emptyMessage,
}: KeywordCardProps) {
  return (
    <Card>
      <CardHeader>
        <div className="flex items-center gap-2">
          <Icon className="size-5 text-primary" />

          <CardTitle>{title}</CardTitle>
        </div>

        <CardDescription>{description}</CardDescription>
      </CardHeader>

      <CardContent>
        {items.length > 0 ? (
          <div className="flex flex-wrap gap-2">
            {items.map((item, index) => (
              <span
                key={`${item}-${index}`}
                className="rounded-full border bg-muted/40 px-3 py-1.5 text-sm"
              >
                {item}
              </span>
            ))}
          </div>
        ) : (
          <EmptyState icon={Search} message={emptyMessage} />
        )}
      </CardContent>
    </Card>
  )
}

interface EmptyStateProps {
  icon: typeof FileText
  message: string
}

function EmptyState({ icon: Icon, message }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center rounded-lg border border-dashed px-6 py-8 text-center">
      <Icon className="size-7 text-muted-foreground" />

      <p className="mt-3 text-sm text-muted-foreground">{message}</p>
    </div>
  )
}

export default ATSOptimizationResult
