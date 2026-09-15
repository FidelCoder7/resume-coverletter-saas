import { ArrowLeft, FileText, LoaderCircle, Mail, Sparkles } from 'lucide-react'
import { useState } from 'react'
import { Link } from 'react-router-dom'

import { buttonVariants } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import CoverLetterGenerationForm from '@/features/ai/components/CoverLetterGenerationForm'
import CoverLetterGenerationResult from '@/features/ai/components/CoverLetterGenerationResult'
import CoverLetterList from '@/features/ai/components/CoverLetterList'
import type { CoverLetter } from '@/features/ai/types'
import { useResumes } from '@/features/resumes/hooks/use_resumes'
import type { Resume } from '@/features/resumes/types'
import { getApiErrorMessage } from '@/utils/api_error'

function CoverLetterGenerator() {
  const [selectedResumeId, setSelectedResumeId] = useState('')
  const [generatedCoverLetter, setGeneratedCoverLetter] =
    useState<CoverLetter | null>(null)

  const { data: resumes = [], isLoading, isError, error } = useResumes()

  function handleGenerated(coverLetter: CoverLetter) {
    setGeneratedCoverLetter(coverLetter)
    setSelectedResumeId(coverLetter.resume_id)
  }

  return (
    <div className="mx-auto w-full max-w-5xl space-y-8">
      <section>
        <Link
          to="/ai"
          className={buttonVariants({
            variant: 'outline',
            size: 'sm',
          })}
        >
          <ArrowLeft />
          Back to AI Workspace
        </Link>

        <div className="mt-6 flex items-center gap-3">
          <div className="flex size-10 items-center justify-center rounded-lg bg-primary/10">
            <Mail className="size-5 text-primary" />
          </div>

          <div>
            <p className="text-sm font-medium text-primary">AI Cover Letter</p>

            <h1 className="text-3xl font-semibold tracking-tight">
              Cover Letter Generator
            </h1>
          </div>
        </div>

        <p className="mt-3 max-w-2xl text-sm leading-6 text-muted-foreground">
          Create a targeted cover letter using the information in your existing
          resume and the requirements of the job you want.
        </p>
      </section>

      <Card>
        <CardHeader>
          <CardTitle>Select a resume</CardTitle>

          <CardDescription>
            Choose the resume you want to use as the foundation for your cover
            letter.
          </CardDescription>
        </CardHeader>

        <CardContent>
          {isLoading ? (
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <LoaderCircle className="size-4 animate-spin" />
              Loading your resumes...
            </div>
          ) : isError ? (
            <div className="rounded-lg border border-destructive/30 bg-destructive/5 px-4 py-3">
              <p className="text-sm text-destructive">
                {getApiErrorMessage(error)}
              </p>
            </div>
          ) : resumes.length === 0 ? (
            <div className="flex flex-col items-start gap-4 rounded-lg border border-dashed px-6 py-8">
              <div className="flex size-10 items-center justify-center rounded-lg bg-muted">
                <FileText className="size-5 text-muted-foreground" />
              </div>

              <div>
                <p className="font-medium">No resumes available</p>

                <p className="mt-1 text-sm text-muted-foreground">
                  Create a resume before using AI cover letter generation.
                </p>
              </div>

              <Link to="/resumes/new" className={buttonVariants()}>
                Create Resume
              </Link>
            </div>
          ) : (
            <div className="space-y-3">
              <label
                htmlFor="resume"
                className="flex items-center gap-2 text-sm leading-none font-medium"
              >
                Resume
              </label>

              <select
                id="resume"
                value={selectedResumeId}
                onChange={(event) => {
                  setSelectedResumeId(event.target.value)
                  setGeneratedCoverLetter(null)
                }}
                className="flex h-9 w-full rounded-lg border border-input bg-background px-3 text-sm outline-none transition-colors focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/50"
              >
                <option value="">Select a resume</option>

                {resumes.map((resume: Resume) => (
                  <option key={resume.id} value={resume.id}>
                    {resume.title}
                    {resume.is_default ? ' (Default)' : ''}
                  </option>
                ))}
              </select>
            </div>
          )}
        </CardContent>
      </Card>

      {selectedResumeId && (
        <>
          <CoverLetterGenerationForm
            key={selectedResumeId}
            resumeId={selectedResumeId}
            onSuccess={handleGenerated}
          />

          <CoverLetterList
            key={`list-${selectedResumeId}`}
            resumeId={selectedResumeId}
          />
        </>
      )}

      {generatedCoverLetter && (
        <CoverLetterGenerationResult coverLetter={generatedCoverLetter} />
      )}

      {!selectedResumeId && resumes.length > 0 && (
        <Card>
          <CardContent className="flex flex-col items-center justify-center px-6 py-12 text-center">
            <div className="flex size-10 items-center justify-center rounded-lg bg-primary/10">
              <Sparkles className="size-5 text-primary" />
            </div>

            <p className="mt-4 font-medium">Select a resume to get started</p>

            <p className="mt-1 max-w-md text-sm text-muted-foreground">
              Your resume provides the professional context the AI needs to
              create a relevant cover letter.
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

export default CoverLetterGenerator
