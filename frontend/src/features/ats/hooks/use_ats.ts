import { useMutation, useQueryClient } from '@tanstack/react-query'

import { optimizeResumeForATS } from '@/features/ats/api/ats_api'

import type {
  ATSOptimizationRequest,
  ATSOptimizationResponse,
} from '@/features/ats/types'

export const atsQueryKeys = {
  all: ['ats'] as const,

  optimizations: () => [...atsQueryKeys.all, 'optimization'] as const,

  optimization: (resumeId: string) =>
    [...atsQueryKeys.optimizations(), resumeId] as const,
}

export function useOptimizeResumeForATS() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({
      resumeId,
      payload,
    }: {
      resumeId: string
      payload: ATSOptimizationRequest
    }) => optimizeResumeForATS(resumeId, payload),

    onSuccess: (result: ATSOptimizationResponse, variables) => {
      queryClient.setQueryData(
        atsQueryKeys.optimization(variables.resumeId),
        result,
      )
    },
  })
}
