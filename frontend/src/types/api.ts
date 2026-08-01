export interface ApiErrorDetail {
  code?: string
  message: string
  field?: string
}

export interface ApiErrorResponse {
  detail: string | ApiErrorDetail | ApiErrorDetail[]
}

export interface ApiResponse<T> {
  data: T
  message?: string
}
