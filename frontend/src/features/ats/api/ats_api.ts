import apiClient from '@/api/axios'
import { API_ENDPOINTS } from '@/api/endpoint'

import type {
  ATSOptimizationRequest,
  ATSOptimizationResponse,
} from '@/features/ats/types'

export async function optimizeResumeForATS(
  resumeId: string,
  payload: ATSOptimizationRequest,
): Promise<ATSOptimizationResponse> {
  const response = await apiClient.post<ATSOptimizationResponse>(
    API_ENDPOINTS.ATS.OPTIMIZE(resumeId),
    payload,
  )

  return response.data
}
