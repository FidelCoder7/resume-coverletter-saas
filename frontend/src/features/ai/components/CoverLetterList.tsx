import { FileText, LoaderCircle, Mail } from 'lucide-react'

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { useCoverLetters } from '@/features/ai/hooks/use_cover_letters'
import { getApiErrorMessage } from '@/utils/api_error'

interface CoverLetterListProps {
  resumeId: string
}

function CoverLetterList({ resumeId }: CoverLetterListProps) {
  const {
    data: coverLetters = [],
    isLoading,
    isError,
    error,
  } = useCoverLetters(resumeId)

  return (
    <Card>
      <CardHeader>
        <CardTitle>Existing Cover Letters</CardTitle>

        <CardDescription>
          Cover letters previously generated for this resume.
        </CardDescription>
      </CardHeader>

      <CardContent>
        {isLoading ? (
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <LoaderCircle className="size-4 animate-spin" />
            Loading cover letters...
          </div>
        ) : isError ? (
          <div className="rounded-lg border border-destructive/30 bg-destructive/5 px-4 py-3">
            <p className="text-sm text-destructive">
              {getApiErrorMessage(error)}
            </p>
          </div>
        ) : coverLetters.length === 0 ? (
          <div className="flex flex-col items-center justify-center rounded-lg border border-dashed px-6 py-10 text-center">
            <Mail className="size-8 text-muted-foreground" />

            <p className="mt-3 text-sm font-medium">No cover letters yet</p>

            <p className="mt-1 max-w-md text-sm text-muted-foreground">
              Generate your first targeted cover letter using the form above.
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {coverLetters.map((coverLetter) => (
              <div
                key={coverLetter.id}
                className="flex flex-col gap-3 rounded-lg border p-4 sm:flex-row sm:items-center sm:justify-between"
              >
                <div className="flex min-w-0 items-start gap-3">
                  <div className="flex size-9 shrink-0 items-center justify-center rounded-lg bg-muted">
                    <FileText className="size-4 text-muted-foreground" />
                  </div>

                  <div className="min-w-0">
                    <p className="truncate font-medium">{coverLetter.title}</p>

                    <p className="mt-1 text-sm text-muted-foreground">
                      {coverLetter.job_title} at {coverLetter.company_name}
                    </p>

                    <p className="mt-1 text-xs text-muted-foreground">
                      Updated {formatDate(coverLetter.updated_at)}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  )
}

function formatDate(value: string) {
  return new Date(value).toLocaleString()
}

export default CoverLetterList
