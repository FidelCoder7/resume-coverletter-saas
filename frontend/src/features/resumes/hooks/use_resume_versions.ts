import {
  useMutation,
  useQuery,
  useQueryClient,
  type UseMutationResult,
  type UseQueryResult,
} from '@tanstack/react-query'

import {
  getLatestResumeVersion,
  getResumeVersion,
  getResumeVersions,
  restoreResumeVersion,
} from '@/features/resumes/api/resume_version_api'
import type { Resume, ResumeVersion } from '@/features/resumes/types'

export const resumeVersionQueryKeys = {
  all: ['resume-versions'] as const,
  lists: () => [...resumeVersionQueryKeys.all, 'list'] as const,
  list: (resumeId: string) =>
    [...resumeVersionQueryKeys.lists(), resumeId] as const,
  details: () => [...resumeVersionQueryKeys.all, 'detail'] as const,
  detail: (resumeId: string, versionId: string) =>
    [...resumeVersionQueryKeys.details(), resumeId, versionId] as const,
  latest: (resumeId: string) =>
    [...resumeVersionQueryKeys.all, 'latest', resumeId] as const,
}

export function useResumeVersions(
  resumeId: string,
): UseQueryResult<ResumeVersion[], Error> {
  return useQuery({
    queryKey: resumeVersionQueryKeys.list(resumeId),
    queryFn: () => getResumeVersions(resumeId),
    enabled: Boolean(resumeId),
  })
}

export function useLatestResumeVersion(
  resumeId: string,
): UseQueryResult<ResumeVersion, Error> {
  return useQuery({
    queryKey: resumeVersionQueryKeys.latest(resumeId),
    queryFn: () => getLatestResumeVersion(resumeId),
    enabled: Boolean(resumeId),
  })
}

export function useResumeVersion(
  resumeId: string,
  versionId: string,
): UseQueryResult<ResumeVersion, Error> {
  return useQuery({
    queryKey: resumeVersionQueryKeys.detail(resumeId, versionId),
    queryFn: () => getResumeVersion(resumeId, versionId),
    enabled: Boolean(resumeId) && Boolean(versionId),
  })
}

interface RestoreResumeVersionVariables {
  resumeId: string
  versionId: string
}

export function useRestoreResumeVersion(): UseMutationResult<
  Resume,
  Error,
  RestoreResumeVersionVariables
> {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ resumeId, versionId }) =>
      restoreResumeVersion(resumeId, versionId),

    onSuccess: (_resume, variables) => {
      queryClient.invalidateQueries({
        queryKey: resumeVersionQueryKeys.list(variables.resumeId),
      })

      queryClient.invalidateQueries({
        queryKey: resumeVersionQueryKeys.latest(variables.resumeId),
      })

      queryClient.invalidateQueries({
        queryKey: [...resumeVersionQueryKeys.details(), variables.resumeId],
      })

      queryClient.invalidateQueries({
        queryKey: ['resumes', 'detail', variables.resumeId],
      })

      queryClient.invalidateQueries({
        queryKey: ['resumes', 'list'],
      })
    },
  })
}
