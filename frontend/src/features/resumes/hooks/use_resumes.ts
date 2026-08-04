import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import {
  createResume,
  deleteResume,
  generateResume,
  getResume,
  listResumes,
  updateResume,
} from '@/features/resumes/api/resume_api'

import type {
  CreateResumeRequest,
  ResumeGenerationRequest,
  UpdateResumeRequest,
} from '@/features/resumes/types'

export const resumeQueryKeys = {
  all: ['resumes'] as const,

  lists: () => [...resumeQueryKeys.all, 'list'] as const,

  list: () => [...resumeQueryKeys.lists()] as const,

  details: () => [...resumeQueryKeys.all, 'detail'] as const,

  detail: (resumeId: string) =>
    [...resumeQueryKeys.details(), resumeId] as const,
}

export function useResumes() {
  return useQuery({
    queryKey: resumeQueryKeys.list(),
    queryFn: listResumes,
  })
}

export function useResume(resumeId: string) {
  return useQuery({
    queryKey: resumeQueryKeys.detail(resumeId),
    queryFn: () => getResume(resumeId),
    enabled: Boolean(resumeId),
  })
}

export function useCreateResume() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (payload: CreateResumeRequest) => createResume(payload),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: resumeQueryKeys.lists(),
      })
    },
  })
}

export function useUpdateResume() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({
      resumeId,
      payload,
    }: {
      resumeId: string
      payload: UpdateResumeRequest
    }) => updateResume(resumeId, payload),

    onSuccess: (resume) => {
      queryClient.setQueryData(resumeQueryKeys.detail(resume.id), resume)

      queryClient.invalidateQueries({
        queryKey: resumeQueryKeys.lists(),
      })
    },
  })
}

export function useDeleteResume() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (resumeId: string) => deleteResume(resumeId),

    onSuccess: (_, resumeId) => {
      queryClient.removeQueries({
        queryKey: resumeQueryKeys.detail(resumeId),
      })

      queryClient.invalidateQueries({
        queryKey: resumeQueryKeys.lists(),
      })
    },
  })
}

export function useGenerateResume() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({
      resumeId,
      payload,
    }: {
      resumeId: string
      payload: ResumeGenerationRequest
    }) => generateResume(resumeId, payload),

    onSuccess: (resume) => {
      queryClient.setQueryData(resumeQueryKeys.detail(resume.id), resume)

      queryClient.invalidateQueries({
        queryKey: resumeQueryKeys.lists(),
      })
    },
  })
}
