import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import {
  generateCoverLetter,
  getCoverLetter,
  listCoverLetters,
  regenerateCoverLetter,
} from '@/features/ai/api/cover_letter_api'

import type {
  CoverLetterGenerationRequest,
  CoverLetterRegenerationRequest,
} from '@/features/ai/types'

export const coverLetterQueryKeys = {
  all: ['cover-letters'] as const,

  lists: () => [...coverLetterQueryKeys.all, 'list'] as const,

  list: (resumeId: string) =>
    [...coverLetterQueryKeys.lists(), resumeId] as const,

  details: () => [...coverLetterQueryKeys.all, 'detail'] as const,

  detail: (coverLetterId: string) =>
    [...coverLetterQueryKeys.details(), coverLetterId] as const,
}

export function useCoverLetters(resumeId: string) {
  return useQuery({
    queryKey: coverLetterQueryKeys.list(resumeId),
    queryFn: () => listCoverLetters(resumeId),
    enabled: Boolean(resumeId),
  })
}

export function useCoverLetter(coverLetterId: string) {
  return useQuery({
    queryKey: coverLetterQueryKeys.detail(coverLetterId),
    queryFn: () => getCoverLetter(coverLetterId),
    enabled: Boolean(coverLetterId),
  })
}

export function useGenerateCoverLetter() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({
      resumeId,
      payload,
    }: {
      resumeId: string
      payload: CoverLetterGenerationRequest
    }) => generateCoverLetter(resumeId, payload),

    onSuccess: (coverLetter) => {
      queryClient.setQueryData(
        coverLetterQueryKeys.detail(coverLetter.id),
        coverLetter,
      )

      queryClient.invalidateQueries({
        queryKey: coverLetterQueryKeys.list(coverLetter.resume_id),
      })
    },
  })
}

export function useRegenerateCoverLetter() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({
      coverLetterId,
      payload,
    }: {
      coverLetterId: string
      payload: CoverLetterRegenerationRequest
    }) => regenerateCoverLetter(coverLetterId, payload),

    onSuccess: (coverLetter) => {
      queryClient.setQueryData(
        coverLetterQueryKeys.detail(coverLetter.id),
        coverLetter,
      )

      queryClient.invalidateQueries({
        queryKey: coverLetterQueryKeys.list(coverLetter.resume_id),
      })
    },
  })
}
