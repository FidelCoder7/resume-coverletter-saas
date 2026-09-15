import apiClient from '@/api/axios'
import { API_ENDPOINTS } from '@/api/endpoint'

import type {
  CoverLetter,
  CoverLetterGenerationRequest,
  CoverLetterListResponse,
  CoverLetterRegenerationRequest,
} from '@/features/ai/types'

export async function listCoverLetters(
  resumeId: string,
): Promise<CoverLetter[]> {
  const response = await apiClient.get<CoverLetterListResponse>(
    API_ENDPOINTS.COVER_LETTERS.BY_RESUME(resumeId),
  )

  return response.data.cover_letters
}

export async function getCoverLetter(
  coverLetterId: string,
): Promise<CoverLetter> {
  const response = await apiClient.get<CoverLetter>(
    API_ENDPOINTS.COVER_LETTERS.BY_ID(coverLetterId),
  )

  return response.data
}

export async function generateCoverLetter(
  resumeId: string,
  payload: CoverLetterGenerationRequest,
): Promise<CoverLetter> {
  const response = await apiClient.post<CoverLetter>(
    API_ENDPOINTS.COVER_LETTERS.GENERATE(resumeId),
    payload,
  )

  return response.data
}

export async function regenerateCoverLetter(
  coverLetterId: string,
  payload: CoverLetterRegenerationRequest,
): Promise<CoverLetter> {
  const response = await apiClient.post<CoverLetter>(
    API_ENDPOINTS.COVER_LETTERS.REGENERATE(coverLetterId),
    payload,
  )

  return response.data
}
