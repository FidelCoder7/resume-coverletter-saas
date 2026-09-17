import { useMutation, type UseMutationResult } from '@tanstack/react-query'

import {
  exportResumeDocx,
  exportResumePdf,
  type ResumeExportResult,
} from '@/features/resumes/api/resume_export_api'

interface ExportResumeVariables {
  resumeId: string
}

export function useExportResumePdf(): UseMutationResult<
  ResumeExportResult,
  Error,
  ExportResumeVariables
> {
  return useMutation({
    mutationFn: ({ resumeId }) => exportResumePdf(resumeId),
  })
}

export function useExportResumeDocx(): UseMutationResult<
  ResumeExportResult,
  Error,
  ExportResumeVariables
> {
  return useMutation({
    mutationFn: ({ resumeId }) => exportResumeDocx(resumeId),
  })
}
