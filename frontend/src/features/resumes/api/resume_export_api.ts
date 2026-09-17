import apiClient from '@/api/axios'
import { API_ENDPOINTS } from '@/api/endpoint'

export interface ResumeExportResult {
  blob: Blob
  filename: string
}

function getFilenameFromContentDisposition(
  contentDisposition: string | undefined,
): string | null {
  if (!contentDisposition) {
    return null
  }

  const utf8Match = contentDisposition.match(/filename\*=UTF-8''([^;]+)/i)

  if (utf8Match?.[1]) {
    return decodeURIComponent(utf8Match[1])
  }

  const filenameMatch = contentDisposition.match(/filename="?([^";]+)"?/i)

  return filenameMatch?.[1] ?? null
}

export async function exportResumePdf(
  resumeId: string,
): Promise<ResumeExportResult> {
  const response = await apiClient.get<Blob>(
    API_ENDPOINTS.RESUMES.EXPORT_PDF(resumeId),
    {
      responseType: 'blob',
    },
  )

  return {
    blob: response.data,
    filename:
      getFilenameFromContentDisposition(
        response.headers['content-disposition'],
      ) ?? 'resume.pdf',
  }
}

export async function exportResumeDocx(
  resumeId: string,
): Promise<ResumeExportResult> {
  const response = await apiClient.get<Blob>(
    API_ENDPOINTS.RESUMES.EXPORT_DOCX(resumeId),
    {
      responseType: 'blob',
    },
  )

  return {
    blob: response.data,
    filename:
      getFilenameFromContentDisposition(
        response.headers['content-disposition'],
      ) ?? 'resume.docx',
  }
}
