import { useQuery } from '@tanstack/react-query'

import {
  getAIFeatureBreakdown,
  getAIUsage,
  getAIUsageDashboard,
  getAIUsageSummary,
  listAIUsage,
  listCoverLetterAIUsage,
  listResumeAIUsage,
} from '@/features/ai_usage/api/ai_usage_api'

export const aiUsageQueryKeys = {
  all: ['ai-usage'] as const,

  history: () => [...aiUsageQueryKeys.all, 'history'] as const,

  usage: (usageId: string) =>
    [...aiUsageQueryKeys.all, 'usage', usageId] as const,

  resumeHistory: (resumeId: string) =>
    [...aiUsageQueryKeys.all, 'resume', resumeId] as const,

  coverLetterHistory: (coverLetterId: string) =>
    [...aiUsageQueryKeys.all, 'cover-letter', coverLetterId] as const,

  summary: (startDate: string, endDate: string) =>
    [...aiUsageQueryKeys.all, 'summary', startDate, endDate] as const,

  features: (startDate: string, endDate: string) =>
    [...aiUsageQueryKeys.all, 'features', startDate, endDate] as const,

  dashboard: (startDate: string, endDate: string) =>
    [...aiUsageQueryKeys.all, 'dashboard', startDate, endDate] as const,
}

export function useAIUsage() {
  return useQuery({
    queryKey: aiUsageQueryKeys.history(),
    queryFn: listAIUsage,
  })
}

export function useAIUsageRecord(usageId: string) {
  return useQuery({
    queryKey: aiUsageQueryKeys.usage(usageId),
    queryFn: () => getAIUsage(usageId),
    enabled: Boolean(usageId),
  })
}

export function useResumeAIUsage(resumeId: string) {
  return useQuery({
    queryKey: aiUsageQueryKeys.resumeHistory(resumeId),
    queryFn: () => listResumeAIUsage(resumeId),
    enabled: Boolean(resumeId),
  })
}

export function useCoverLetterAIUsage(coverLetterId: string) {
  return useQuery({
    queryKey: aiUsageQueryKeys.coverLetterHistory(coverLetterId),
    queryFn: () => listCoverLetterAIUsage(coverLetterId),
    enabled: Boolean(coverLetterId),
  })
}

export function useAIUsageSummary(startDate: string, endDate: string) {
  return useQuery({
    queryKey: aiUsageQueryKeys.summary(startDate, endDate),
    queryFn: () =>
      getAIUsageSummary({
        start_date: startDate,
        end_date: endDate,
      }),
    enabled: Boolean(startDate && endDate),
  })
}

export function useAIFeatureBreakdown(startDate: string, endDate: string) {
  return useQuery({
    queryKey: aiUsageQueryKeys.features(startDate, endDate),
    queryFn: () =>
      getAIFeatureBreakdown({
        start_date: startDate,
        end_date: endDate,
      }),
    enabled: Boolean(startDate && endDate),
  })
}

export function useAIUsageDashboard(startDate: string, endDate: string) {
  return useQuery({
    queryKey: aiUsageQueryKeys.dashboard(startDate, endDate),
    queryFn: () =>
      getAIUsageDashboard({
        start_date: startDate,
        end_date: endDate,
      }),
    enabled: Boolean(startDate && endDate),
  })
}
