import apiClient from '@/api/axios'
import { API_ENDPOINTS } from '@/api/endpoint'

import type {
  Certification,
  CertificationListResponse,
  CreateCertificationRequest,
  UpdateCertificationRequest,
} from '@/features/resumes/types'

export async function listCertifications(
  resumeId: string,
): Promise<Certification[]> {
  const response = await apiClient.get<CertificationListResponse>(
    API_ENDPOINTS.CERTIFICATIONS.BY_RESUME(resumeId),
  )

  return response.data.certifications
}

export async function createCertification(
  resumeId: string,
  payload: CreateCertificationRequest,
): Promise<Certification> {
  const response = await apiClient.post<Certification>(
    API_ENDPOINTS.CERTIFICATIONS.BY_RESUME(resumeId),
    payload,
  )

  return response.data
}

export async function updateCertification(
  certificationId: string,
  payload: UpdateCertificationRequest,
): Promise<Certification> {
  const response = await apiClient.put<Certification>(
    API_ENDPOINTS.CERTIFICATIONS.BY_ID(certificationId),
    payload,
  )

  return response.data
}

export async function deleteCertification(
  certificationId: string,
): Promise<void> {
  await apiClient.delete(API_ENDPOINTS.CERTIFICATIONS.BY_ID(certificationId))
}
