import apiClient from '@/api/axios'
import { API_ENDPOINTS } from '@/api/endpoint'

import type {
  CreateProjectRequest,
  Project,
  ProjectListResponse,
  UpdateProjectRequest,
} from '@/features/resumes/types'

export async function listProjects(resumeId: string): Promise<Project[]> {
  const response = await apiClient.get<ProjectListResponse>(
    API_ENDPOINTS.PROJECTS.BY_RESUME(resumeId),
  )

  return response.data.projects
}

export async function createProject(
  resumeId: string,
  payload: CreateProjectRequest,
): Promise<Project> {
  const response = await apiClient.post<Project>(
    API_ENDPOINTS.PROJECTS.BY_RESUME(resumeId),
    payload,
  )

  return response.data
}

export async function updateProject(
  projectId: string,
  payload: UpdateProjectRequest,
): Promise<Project> {
  const response = await apiClient.put<Project>(
    API_ENDPOINTS.PROJECTS.BY_ID(projectId),
    payload,
  )

  return response.data
}

export async function deleteProject(projectId: string): Promise<void> {
  await apiClient.delete(API_ENDPOINTS.PROJECTS.BY_ID(projectId))
}
