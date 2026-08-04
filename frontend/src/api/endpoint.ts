export const API_ENDPOINTS = {
  AUTH: {
    BASE: '/auth',
    REGISTER: '/auth/register',
    LOGIN: '/auth/login',
    REFRESH: '/auth/refresh',
    LOGOUT: '/auth/logout',
    ME: '/auth/me',
    VERIFY_EMAIL: '/auth/verify-email',
    FORGOT_PASSWORD: '/auth/forgot-password',
    RESET_PASSWORD: '/auth/reset-password',
    GOOGLE_LOGIN: '/auth/google/login',
  },

  USERS: '/users',

  RESUMES: {
    BASE: '/api/resumes',
    IMPORT: '/api/resumes/import',
    BY_ID: (resumeId: string) => `/api/resumes/${resumeId}`,
    GENERATE: (resumeId: string) => `/api/resumes/${resumeId}/generate`,
  },

  EXPERIENCES: {
    BY_RESUME: (resumeId: string) => `/api/experiences/resume/${resumeId}`,
    BY_ID: (experienceId: string) => `/api/experiences/${experienceId}`,
  },

  EDUCATIONS: {
    BY_RESUME: (resumeId: string) => `/api/educations/resume/${resumeId}`,
    BY_ID: (educationId: string) => `/api/educations/${educationId}`,
  },

  SKILLS: {
    BY_RESUME: (resumeId: string) => `/api/skills/resume/${resumeId}`,
    BY_ID: (skillId: string) => `/api/skills/${skillId}`,
  },

  PROJECTS: {
    BY_RESUME: (resumeId: string) => `/api/projects/resume/${resumeId}`,
    BY_ID: (projectId: string) => `/api/projects/${projectId}`,
  },

  CERTIFICATIONS: {
    BY_RESUME: (resumeId: string) => `/api/certifications/resume/${resumeId}`,
    BY_ID: (certificationId: string) =>
      `/api/certifications/${certificationId}`,
  },

  AI: '/ai',
  SUBSCRIPTIONS: '/subscriptions',
  BILLING: '/billing',
  ADMIN: '/admin',
} as const
