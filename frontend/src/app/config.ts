const apiBaseUrl = import.meta.env.VITE_API_BASE_URL
const appName = import.meta.env.VITE_APP_NAME

if (!apiBaseUrl) {
  throw new Error('VITE_API_BASE_URL is not configured.')
}

if (!appName) {
  throw new Error('VITE_APP_NAME is not configured.')
}

export const appConfig = {
  apiBaseUrl,
  appName,
  mode: import.meta.env.MODE,
  isDevelopment: import.meta.env.DEV,
  isProduction: import.meta.env.PROD,
} as const
