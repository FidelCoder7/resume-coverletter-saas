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
import type { Resume } from '@/features/resumes/types'

interface ResumeGenerationResultProps {
  resume: Resume
}

function ResumeGenerationResult({ resume }: ResumeGenerationResultProps) {
  const [copied, setCopied] = useState(false)

  async function handleCopy() {
    if (!resume.generated_content) {
      return
    }

    await navigator.clipboard.writeText(resume.generated_content)

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

              <CardTitle>Generated Resume</CardTitle>
            </div>

            <CardDescription className="mt-1">
              AI-generated content for {resume.title}.
            </CardDescription>
          </div>

          {resume.generated_content && (
            <Button variant="outline" size="sm" onClick={handleCopy}>
              <Copy />

              {copied ? 'Copied' : 'Copy'}
            </Button>
          )}
        </div>
      </CardHeader>

      <CardContent>
        {resume.generated_content ? (
          <div className="rounded-lg border bg-muted/20 p-4">
            <p className="whitespace-pre-wrap text-sm leading-7">
              {resume.generated_content}
            </p>
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center rounded-lg border border-dashed px-6 py-12 text-center">
            <FileText className="size-8 text-muted-foreground" />

            <p className="mt-3 text-sm font-medium">
              No generated content returned
            </p>

            <p className="mt-1 text-sm text-muted-foreground">
              The resume was processed, but the API did not return generated
              content.
            </p>
          </div>
        )}

        {resume.generated_at && (
          <p className="mt-4 text-xs text-muted-foreground">
            Generated {formatDate(resume.generated_at)}
          </p>
        )}
      </CardContent>
    </Card>
  )
}

function formatDate(value: string) {
  return new Date(value).toLocaleString()
}

export default ResumeGenerationResult
