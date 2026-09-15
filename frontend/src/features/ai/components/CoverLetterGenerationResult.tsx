import { CheckCircle2, Copy, FileText } from 'lucide-react'
import { useState } from 'react'

import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import type { CoverLetter } from '@/features/ai/types'

interface CoverLetterGenerationResultProps {
  coverLetter: CoverLetter
}

function CoverLetterGenerationResult({
  coverLetter,
}: CoverLetterGenerationResultProps) {
  const [copied, setCopied] = useState(false)

  async function handleCopy() {
    if (!coverLetter.content) {
      return
    }

    await navigator.clipboard.writeText(coverLetter.content)

    setCopied(true)

    window.setTimeout(() => {
      setCopied(false)
    }, 2000)
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
          <div>
            <div className="flex items-center gap-2">
              <CheckCircle2 className="size-5 text-primary" />

              <CardTitle>{coverLetter.title}</CardTitle>
            </div>

            <CardDescription className="mt-1">
              {coverLetter.job_title} at {coverLetter.company_name}
            </CardDescription>
          </div>

          {coverLetter.content && (
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
        {coverLetter.content ? (
          <div className="rounded-lg border bg-muted/20 p-6">
            <p className="whitespace-pre-wrap text-sm leading-7">
              {coverLetter.content}
            </p>
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center rounded-lg border border-dashed px-6 py-12 text-center">
            <FileText className="size-8 text-muted-foreground" />

            <p className="mt-3 text-sm font-medium">
              No generated content returned
            </p>

            <p className="mt-1 text-sm text-muted-foreground">
              The cover letter was processed, but the API did not return
              generated content.
            </p>
          </div>
        )}

        <p className="mt-4 text-xs text-muted-foreground">
          Generated {formatDate(coverLetter.updated_at)}
        </p>
      </CardContent>
    </Card>
  )
}

function formatDate(value: string) {
  return new Date(value).toLocaleString()
}

export default CoverLetterGenerationResult
