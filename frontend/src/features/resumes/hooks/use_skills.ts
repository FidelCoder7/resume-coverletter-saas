import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import {
  createSkill,
  deleteSkill,
  listSkills,
  updateSkill,
} from '@/features/resumes/api/skills_api'

import type {
  CreateSkillRequest,
  UpdateSkillRequest,
} from '@/features/resumes/types'

export const skillQueryKeys = {
  all: ['skills'] as const,

  lists: () => [...skillQueryKeys.all, 'list'] as const,

  list: (resumeId: string) => [...skillQueryKeys.lists(), resumeId] as const,

  details: () => [...skillQueryKeys.all, 'detail'] as const,

  detail: (skillId: string) => [...skillQueryKeys.details(), skillId] as const,
}

export function useSkills(resumeId: string) {
  return useQuery({
    queryKey: skillQueryKeys.list(resumeId),
    queryFn: () => listSkills(resumeId),
    enabled: Boolean(resumeId),
  })
}

export function useCreateSkill() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({
      resumeId,
      payload,
    }: {
      resumeId: string
      payload: CreateSkillRequest
    }) => createSkill(resumeId, payload),

    onSuccess: (skill) => {
      queryClient.invalidateQueries({
        queryKey: skillQueryKeys.list(skill.resume_id),
      })
    },
  })
}

export function useUpdateSkill() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({
      skillId,
      payload,
    }: {
      skillId: string
      payload: UpdateSkillRequest
    }) => updateSkill(skillId, payload),

    onSuccess: (skill) => {
      queryClient.setQueryData(skillQueryKeys.detail(skill.id), skill)

      queryClient.invalidateQueries({
        queryKey: skillQueryKeys.list(skill.resume_id),
      })
    },
  })
}

export function useDeleteSkill() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ skillId }: { skillId: string; resumeId: string }) =>
      deleteSkill(skillId),

    onSuccess: (_, variables) => {
      queryClient.removeQueries({
        queryKey: skillQueryKeys.detail(variables.skillId),
      })

      queryClient.invalidateQueries({
        queryKey: skillQueryKeys.list(variables.resumeId),
      })
    },
  })
}
