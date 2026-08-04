import apiClient from '@/api/axios'
import { API_ENDPOINTS } from '@/api/endpoint'

import type {
  CreateEducationRequest,
  Education,
  UpdateEducationRequest,
} from '@/features/resumes/types'

export async function listEducations(resumeId: string): Promise<Education[]> {
  const response = await apiClient.get<Education[]>(
    API_ENDPOINTS.EDUCATIONS.BY_RESUME(resumeId),
  )

  return response.data
}

export async function createEducation(
  resumeId: string,
  payload: CreateEducationRequest,
): Promise<Education> {
  const response = await apiClient.post<Education>(
    API_ENDPOINTS.EDUCATIONS.BY_RESUME(resumeId),
    payload,
  )

  return response.data
}

export async function updateEducation(
  educationId: string,
  payload: UpdateEducationRequest,
): Promise<Education> {
  const response = await apiClient.put<Education>(
    API_ENDPOINTS.EDUCATIONS.BY_ID(educationId),
    payload,
  )

  return response.data
}

export async function deleteEducation(educationId: string): Promise<void> {
  await apiClient.delete(API_ENDPOINTS.EDUCATIONS.BY_ID(educationId))
}
