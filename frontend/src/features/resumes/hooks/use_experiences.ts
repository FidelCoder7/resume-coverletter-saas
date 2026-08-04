import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import {
  createExperience,
  deleteExperience,
  listExperiences,
  updateExperience,
} from '@/features/resumes/api/experience_api'

import type {
  CreateExperienceRequest,
  UpdateExperienceRequest,
} from '@/features/resumes/types'

export const experienceQueryKeys = {
  all: ['experiences'] as const,

  lists: () => [...experienceQueryKeys.all, 'list'] as const,

  list: (resumeId: string) =>
    [...experienceQueryKeys.lists(), resumeId] as const,

  details: () => [...experienceQueryKeys.all, 'detail'] as const,

  detail: (experienceId: string) =>
    [...experienceQueryKeys.details(), experienceId] as const,
}

export function useExperiences(resumeId: string) {
  return useQuery({
    queryKey: experienceQueryKeys.list(resumeId),
    queryFn: () => listExperiences(resumeId),
    enabled: Boolean(resumeId),
  })
}

export function useCreateExperience() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({
      resumeId,
      payload,
    }: {
      resumeId: string
      payload: CreateExperienceRequest
    }) => createExperience(resumeId, payload),

    onSuccess: (experience) => {
      queryClient.invalidateQueries({
        queryKey: experienceQueryKeys.list(experience.resume_id),
      })
    },
  })
}

export function useUpdateExperience() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({
      experienceId,
      payload,
    }: {
      experienceId: string
      payload: UpdateExperienceRequest
    }) => updateExperience(experienceId, payload),

    onSuccess: (experience) => {
      queryClient.setQueryData(
        experienceQueryKeys.detail(experience.id),
        experience,
      )

      queryClient.invalidateQueries({
        queryKey: experienceQueryKeys.list(experience.resume_id),
      })
    },
  })
}

export function useDeleteExperience() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (experience: { experienceId: string; resumeId: string }) =>
      deleteExperience(experience.experienceId),

    onSuccess: (_, variables) => {
      queryClient.removeQueries({
        queryKey: experienceQueryKeys.detail(variables.experienceId),
      })

      queryClient.invalidateQueries({
        queryKey: experienceQueryKeys.list(variables.resumeId),
      })
    },
  })
}
