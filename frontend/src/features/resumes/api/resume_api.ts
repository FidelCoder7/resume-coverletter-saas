import apiClient from '@/api/axios'
import { API_ENDPOINTS } from '@/api/endpoint'

import type {
  CreateResumeRequest,
  Resume,
  ResumeGenerationRequest,
  ResumeListResponse,
  UpdateResumeRequest,
} from '@/features/resumes/types'

export async function listResumes(): Promise<Resume[]> {
  const response = await apiClient.get<ResumeListResponse>(
    API_ENDPOINTS.RESUMES.BASE,
  )

  return response.data.resumes
}

export async function getResume(resumeId: string): Promise<Resume> {
  const response = await apiClient.get<Resume>(
    API_ENDPOINTS.RESUMES.BY_ID(resumeId),
  )

  return response.data
}

export async function createResume(
  payload: CreateResumeRequest,
): Promise<Resume> {
  const response = await apiClient.post<Resume>(
    API_ENDPOINTS.RESUMES.BASE,
    payload,
  )

  return response.data
}

export async function updateResume(
  resumeId: string,
  payload: UpdateResumeRequest,
): Promise<Resume> {
  const response = await apiClient.put<Resume>(
    API_ENDPOINTS.RESUMES.BY_ID(resumeId),
    payload,
  )

  return response.data
}

export async function deleteResume(resumeId: string): Promise<void> {
  await apiClient.delete(API_ENDPOINTS.RESUMES.BY_ID(resumeId))
}

export async function generateResume(
  resumeId: string,
  payload: ResumeGenerationRequest,
): Promise<Resume> {
  const response = await apiClient.post<Resume>(
    API_ENDPOINTS.RESUMES.GENERATE(resumeId),
    payload,
  )

  return response.data
}
