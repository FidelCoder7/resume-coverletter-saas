import { FileDown, FileText, Loader2 } from 'lucide-react'

import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'

import {
  useExportResumeDocx,
  useExportResumePdf,
} from '@/features/resumes/hooks/use_resume_export'
import { getApiErrorMessage } from '@/utils/api_error'

interface ResumeExportActionsProps {
  resumeId: string
}

function ResumeExportActions({ resumeId }: ResumeExportActionsProps) {
  const pdfMutation = useExportResumePdf()
  const docxMutation = useExportResumeDocx()

  const isExporting = pdfMutation.isPending || docxMutation.isPending

  const handlePdfExport = () => {
    pdfMutation.mutate(
      { resumeId },
      {
        onSuccess: ({ blob, filename }) => {
          downloadBlob(blob, filename)
        },
      },
    )
  }

  const handleDocxExport = () => {
    docxMutation.mutate(
      { resumeId },
      {
        onSuccess: ({ blob, filename }) => {
          downloadBlob(blob, filename)
        },
      },
    )
  }

  const exportError = pdfMutation.isError
    ? pdfMutation.error
    : docxMutation.isError
      ? docxMutation.error
      : null

  return (
    <Card>
      <CardHeader>
        <CardTitle>Export Resume</CardTitle>

        <CardDescription>
          Download this resume as a PDF or Microsoft Word document.
        </CardDescription>
      </CardHeader>

      <CardContent className="space-y-4">
        <div className="flex flex-wrap gap-2">
          <Button
            variant="outline"
            onClick={handlePdfExport}
            disabled={isExporting}
          >
            {pdfMutation.isPending ? (
              <>
                <Loader2 className="animate-spin" />
                Exporting PDF...
              </>
            ) : (
              <>
                <FileDown />
                Export PDF
              </>
            )}
          </Button>

          <Button
            variant="outline"
            onClick={handleDocxExport}
            disabled={isExporting}
          >
            {docxMutation.isPending ? (
              <>
                <Loader2 className="animate-spin" />
                Exporting DOCX...
              </>
            ) : (
              <>
                <FileText />
                Export DOCX
              </>
            )}
          </Button>
        </div>

        {exportError && (
          <div className="rounded-lg border border-destructive/20 bg-destructive/5 px-4 py-3">
            <p className="text-sm font-medium text-destructive">
              Unable to export resume.
            </p>

            <p className="mt-1 text-sm text-muted-foreground">
              {getApiErrorMessage(exportError)}
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  )
}

function downloadBlob(blob: Blob, filename: string) {
  const url = URL.createObjectURL(blob)

  const link = document.createElement('a')
  link.href = url
  link.download = filename
  document.body.appendChild(link)
  link.click()
  link.remove()

  URL.revokeObjectURL(url)
}

export default ResumeExportActions
