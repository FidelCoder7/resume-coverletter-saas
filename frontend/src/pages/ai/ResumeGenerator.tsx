import { ArrowLeft, FileText, LoaderCircle, Sparkles } from 'lucide-react'
import { Link } from 'react-router-dom'
import { useState } from 'react'

import { buttonVariants } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { useResumes } from '@/features/resumes/hooks/use_resumes'
import type { Resume } from '@/features/resumes/types'
import ResumeGenerationForm from '@/features/ai/components/ResumeGenerationForm'
import ResumeGenerationResult from '@/features/ai/components/ResumeGenerationResult'
import { getApiErrorMessage } from '@/utils/api_error'

function ResumeGenerator() {
  const [selectedResumeId, setSelectedResumeId] = useState('')
  const [generatedResume, setGeneratedResume] = useState<Resume | null>(null)

  const { data: resumes = [], isLoading, isError, error } = useResumes()

  function handleGenerated(resume: Resume) {
    setGeneratedResume(resume)
    setSelectedResumeId(resume.id)
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
            <Sparkles className="size-5 text-primary" />
          </div>

          <div>
            <p className="text-sm font-medium text-primary">AI Resume</p>

            <h1 className="text-3xl font-semibold tracking-tight">
              Resume Generator
            </h1>
          </div>
        </div>

        <p className="mt-3 max-w-2xl text-sm leading-6 text-muted-foreground">
          Generate tailored resume content using your existing resume data and
          an optional target job description.
        </p>
      </section>

      <Card>
        <CardHeader>
          <CardTitle>Select a resume</CardTitle>

          <CardDescription>
            Choose the resume you want AI to generate or improve.
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
                  Create a resume before using AI resume generation.
                </p>
              </div>

              <Link to="/resumes/new" className={buttonVariants()}>
                Create Resume
              </Link>
            </div>
          ) : (
            <div className="space-y-2">
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
                  setGeneratedResume(null)
                }}
                className="flex h-9 w-full rounded-lg border border-input bg-background px-3 text-sm outline-none transition-colors focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/50"
              >
                <option value="">Select a resume</option>

                {resumes.map((resume) => (
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
        <ResumeGenerationForm
          key={selectedResumeId}
          resumeId={selectedResumeId}
          onSuccess={handleGenerated}
        />
      )}

      {generatedResume && <ResumeGenerationResult resume={generatedResume} />}
    </div>
  )
}

export default ResumeGenerator
