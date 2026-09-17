import apiClient from '@/api/axios'
import { API_ENDPOINTS } from '@/api/endpoint'
import type { Resume, ResumeVersion } from '@/features/resumes/types'

export async function getResumeVersions(
  resumeId: string,
): Promise<ResumeVersion[]> {
  const response = await apiClient.get<ResumeVersion[]>(
    API_ENDPOINTS.RESUMES.VERSIONS(resumeId),
  )

  return response.data
}

export async function getLatestResumeVersion(
  resumeId: string,
): Promise<ResumeVersion> {
  const response = await apiClient.get<ResumeVersion>(
    API_ENDPOINTS.RESUMES.LATEST_VERSION(resumeId),
  )

  return response.data
}

export async function getResumeVersion(
  resumeId: string,
  versionId: string,
): Promise<ResumeVersion> {
  const response = await apiClient.get<ResumeVersion>(
    API_ENDPOINTS.RESUMES.VERSION_BY_ID(resumeId, versionId),
  )

  return response.data
}

export async function restoreResumeVersion(
  resumeId: string,
  versionId: string,
): Promise<Resume> {
  const response = await apiClient.post<Resume>(
    API_ENDPOINTS.RESUMES.RESTORE_VERSION(resumeId, versionId),
  )

  return response.data
}
