import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import {
  createProject,
  deleteProject,
  listProjects,
  updateProject,
} from '@/features/resumes/api/project_api'

import type {
  CreateProjectRequest,
  UpdateProjectRequest,
} from '@/features/resumes/types'

const projectKeys = {
  all: ['projects'] as const,
  byResume: (resumeId: string) =>
    [...projectKeys.all, 'resume', resumeId] as const,
}

export function useProjects(resumeId: string) {
  return useQuery({
    queryKey: projectKeys.byResume(resumeId),
    queryFn: () => listProjects(resumeId),
    enabled: Boolean(resumeId),
  })
}

export function useCreateProject() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({
      resumeId,
      payload,
    }: {
      resumeId: string
      payload: CreateProjectRequest
    }) => createProject(resumeId, payload),

    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: projectKeys.byResume(variables.resumeId),
      })
    },
  })
}

export function useUpdateProject() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({
      projectId,
      payload,
    }: {
      projectId: string
      resumeId: string
      payload: UpdateProjectRequest
    }) => updateProject(projectId, payload),

    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: projectKeys.byResume(variables.resumeId),
      })
    },
  })
}
export function useDeleteProject() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ projectId }: { projectId: string; resumeId: string }) =>
      deleteProject(projectId),

    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: projectKeys.byResume(variables.resumeId),
      })
    },
  })
}
