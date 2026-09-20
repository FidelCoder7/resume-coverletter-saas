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

    VERSIONS: (resumeId: string) => `/api/resumes/${resumeId}/versions`,
    LATEST_VERSION: (resumeId: string) =>
      `/api/resumes/${resumeId}/versions/latest`,
    VERSION_BY_ID: (resumeId: string, versionId: string) =>
      `/api/resumes/${resumeId}/versions/${versionId}`,
    RESTORE_VERSION: (resumeId: string, versionId: string) =>
      `/api/resumes/${resumeId}/versions/${versionId}/restore`,

    EXPORT_PDF: (resumeId: string) => `/api/resumes/${resumeId}/export/pdf`,
    EXPORT_DOCX: (resumeId: string) => `/api/resumes/${resumeId}/export/docx`,
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

  COVER_LETTERS: {
    BY_RESUME: (resumeId: string) => `/api/cover-letters/resume/${resumeId}`,
    GENERATE: (resumeId: string) =>
      `/api/cover-letters/resume/${resumeId}/generate`,
    BY_ID: (coverLetterId: string) => `/api/cover-letters/${coverLetterId}`,
    REGENERATE: (coverLetterId: string) =>
      `/api/cover-letters/${coverLetterId}/regenerate`,
  },

  ATS: {
    OPTIMIZE: (resumeId: string) => `/api/ats/optimize/${resumeId}`,
  },

  AI_USAGE: {
    BASE: '/api/ai-usage',
    BY_ID: (usageId: string) => `/api/ai-usage/${usageId}`,
    BY_RESUME: (resumeId: string) => `/api/ai-usage/resume/${resumeId}`,
    BY_COVER_LETTER: (coverLetterId: string) =>
      `/api/ai-usage/cover-letter/${coverLetterId}`,
    SUMMARY: '/api/ai-usage/summary',
    FEATURES: '/api/ai-usage/features',
    DASHBOARD: '/api/ai-usage/dashboard',
  },

  SUBSCRIPTIONS: {
    BASE: '/api/subscriptions',
    LIMITS: '/api/subscriptions/limits',
    USAGE: '/api/subscriptions/usage',
  },

  BILLING: {
    BASE: '/api/billing',
    PAYMENTS: '/api/billing/payments',
    CALLBACK: '/api/billing/payments/callback',
    TRANSACTIONS: '/api/billing/transactions',
    TRANSACTION_BY_ID: (transactionId: string) =>
      `/api/billing/transactions/${transactionId}`,
    TRANSACTION_STATUS: (transactionId: string) =>
      `/api/billing/transactions/${transactionId}/status`,
  },

  ADMIN: {
    BASE: '/api/admin',
    ACCESS: '/api/admin/access',
    USERS: '/api/admin/users',
    USER_BY_ID: (userId: string) => `/api/admin/users/${userId}`,
    SUSPEND_USER: (userId: string) => `/api/admin/users/${userId}/suspend`,
    REACTIVATE_USER: (userId: string) =>
      `/api/admin/users/${userId}/reactivate`,
    AUDIT_LOGS: '/api/admin/audit-logs',
    AUDIT_LOG_BY_ID: (auditLogId: string) =>
      `/api/admin/audit-logs/${auditLogId}`,
    USER_AUDIT_LOGS: (userId: string) =>
      `/api/admin/users/${userId}/audit-logs`,
    ADMIN_AUDIT_LOGS: (adminId: string) =>
      `/api/admin/admins/${adminId}/audit-logs`,
    METRICS: '/api/admin/metrics',
    METRICS_TIMESERIES: '/api/admin/metrics/timeseries',
  } as const,
} as const
