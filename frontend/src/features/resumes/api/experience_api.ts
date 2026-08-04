import apiClient from '@/api/axios'
import { API_ENDPOINTS } from '@/api/endpoint'

import type {
  CreateExperienceRequest,
  Experience,
  ExperienceListResponse,
  UpdateExperienceRequest,
} from '@/features/resumes/types'

export async function listExperiences(resumeId: string): Promise<Experience[]> {
  const response = await apiClient.get<ExperienceListResponse>(
    API_ENDPOINTS.EXPERIENCES.BY_RESUME(resumeId),
  )

  return response.data.experiences
}

export async function createExperience(
  resumeId: string,
  payload: CreateExperienceRequest,
): Promise<Experience> {
  const response = await apiClient.post<Experience>(
    API_ENDPOINTS.EXPERIENCES.BY_RESUME(resumeId),
    payload,
  )

  return response.data
}

export async function updateExperience(
  experienceId: string,
  payload: UpdateExperienceRequest,
): Promise<Experience> {
  const response = await apiClient.put<Experience>(
    API_ENDPOINTS.EXPERIENCES.BY_ID(experienceId),
    payload,
  )

  return response.data
}

export async function deleteExperience(experienceId: string): Promise<void> {
  await apiClient.delete(API_ENDPOINTS.EXPERIENCES.BY_ID(experienceId))
}
