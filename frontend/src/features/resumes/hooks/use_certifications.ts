import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import {
  createCertification,
  deleteCertification,
  listCertifications,
  updateCertification,
} from '@/features/resumes/api/certification_api'

import type {
  CreateCertificationRequest,
  UpdateCertificationRequest,
} from '@/features/resumes/types'

const certificationKeys = {
  all: ['certifications'] as const,

  byResume: (resumeId: string) =>
    [...certificationKeys.all, 'resume', resumeId] as const,
}

export function useCertifications(resumeId: string) {
  return useQuery({
    queryKey: certificationKeys.byResume(resumeId),
    queryFn: () => listCertifications(resumeId),
    enabled: Boolean(resumeId),
  })
}

export function useCreateCertification() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({
      resumeId,
      payload,
    }: {
      resumeId: string
      payload: CreateCertificationRequest
    }) => createCertification(resumeId, payload),

    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: certificationKeys.byResume(variables.resumeId),
      })
    },
  })
}

export function useUpdateCertification() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({
      certificationId,
      payload,
    }: {
      certificationId: string
      resumeId: string
      payload: UpdateCertificationRequest
    }) => updateCertification(certificationId, payload),

    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: certificationKeys.byResume(variables.resumeId),
      })
    },
  })
}

export function useDeleteCertification() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({
      certificationId,
    }: {
      certificationId: string
      resumeId: string
    }) => deleteCertification(certificationId),

    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: certificationKeys.byResume(variables.resumeId),
      })
    },
  })
}
