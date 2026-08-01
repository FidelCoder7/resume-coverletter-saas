import axios from 'axios'
import type { ApiErrorDetail } from '@/types/api'

export function getApiErrorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const detail = error.response?.data?.detail

    if (typeof detail === 'string') {
      return detail
    }

    if (Array.isArray(detail)) {
      return detail.map((item: ApiErrorDetail) => item.message).join(', ')
    }

    if (detail && typeof detail === 'object' && 'message' in detail) {
      return String(detail.message)
    }

    if (error.message) {
      return error.message
    }
  }

  if (error instanceof Error) {
    return error.message
  }

  return 'An unexpected error occurred.'
}
