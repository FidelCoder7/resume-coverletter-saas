import apiClient from '@/api/axios'
import { API_ENDPOINTS } from '@/api/endpoint'

import type {
  CreateSkillRequest,
  Skill,
  SkillListResponse,
  UpdateSkillRequest,
} from '@/features/resumes/types'

export async function listSkills(resumeId: string): Promise<Skill[]> {
  const response = await apiClient.get<SkillListResponse>(
    API_ENDPOINTS.SKILLS.BY_RESUME(resumeId),
  )

  return response.data.skills
}

export async function createSkill(
  resumeId: string,
  payload: CreateSkillRequest,
): Promise<Skill> {
  const response = await apiClient.post<Skill>(
    API_ENDPOINTS.SKILLS.BY_RESUME(resumeId),
    payload,
  )

  return response.data
}

export async function updateSkill(
  skillId: string,
  payload: UpdateSkillRequest,
): Promise<Skill> {
  const response = await apiClient.put<Skill>(
    API_ENDPOINTS.SKILLS.BY_ID(skillId),
    payload,
  )

  return response.data
}

export async function deleteSkill(skillId: string): Promise<void> {
  await apiClient.delete(API_ENDPOINTS.SKILLS.BY_ID(skillId))
}
