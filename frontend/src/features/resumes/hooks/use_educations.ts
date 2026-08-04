import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import {
  createEducation,
  deleteEducation,
  listEducations,
  updateEducation,
} from '@/features/resumes/api/education_api'

import type {
  CreateEducationRequest,
  UpdateEducationRequest,
} from '@/features/resumes/types'

export const educationQueryKeys = {
  all: ['educations'] as const,

  lists: () => [...educationQueryKeys.all, 'list'] as const,

  list: (resumeId: string) =>
    [...educationQueryKeys.lists(), resumeId] as const,

  details: () => [...educationQueryKeys.all, 'detail'] as const,

  detail: (educationId: string) =>
    [...educationQueryKeys.details(), educationId] as const,
}

export function useEducations(resumeId: string) {
  return useQuery({
    queryKey: educationQueryKeys.list(resumeId),
    queryFn: () => listEducations(resumeId),
    enabled: Boolean(resumeId),
  })
}

export function useCreateEducation() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({
      resumeId,
      payload,
    }: {
      resumeId: string
      payload: CreateEducationRequest
    }) => createEducation(resumeId, payload),

    onSuccess: (education) => {
      queryClient.invalidateQueries({
        queryKey: educationQueryKeys.list(education.resume_id),
      })
    },
  })
}

export function useUpdateEducation() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({
      educationId,
      payload,
    }: {
      educationId: string
      payload: UpdateEducationRequest
    }) => updateEducation(educationId, payload),

    onSuccess: (education) => {
      queryClient.setQueryData(
        educationQueryKeys.detail(education.id),
        education,
      )

      queryClient.invalidateQueries({
        queryKey: educationQueryKeys.list(education.resume_id),
      })
    },
  })
}

export function useDeleteEducation() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (education: { educationId: string; resumeId: string }) =>
      deleteEducation(education.educationId),

    onSuccess: (_, variables) => {
      queryClient.removeQueries({
        queryKey: educationQueryKeys.detail(variables.educationId),
      })

      queryClient.invalidateQueries({
        queryKey: educationQueryKeys.list(variables.resumeId),
      })
    },
  })
}
