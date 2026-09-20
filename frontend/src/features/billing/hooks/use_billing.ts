import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import {
  getPaymentTransaction,
  initiatePayment,
  listPaymentTransactions,
  synchronizePaymentStatus,
} from '@/features/billing/api/billing_api'

import type {
  PaymentInitiationRequest,
  PaymentStatus,
} from '@/features/billing/types'

export const billingQueryKeys = {
  all: ['billing'] as const,

  transactions: () => [...billingQueryKeys.all, 'transactions'] as const,

  transactionList: (status?: PaymentStatus) =>
    [...billingQueryKeys.transactions(), 'list', status ?? 'all'] as const,

  transaction: (transactionId: string) =>
    [...billingQueryKeys.transactions(), 'detail', transactionId] as const,
}

export function usePaymentTransactions(status?: PaymentStatus) {
  return useQuery({
    queryKey: billingQueryKeys.transactionList(status),
    queryFn: () => listPaymentTransactions(status),
  })
}

export function usePaymentTransaction(transactionId: string) {
  return useQuery({
    queryKey: billingQueryKeys.transaction(transactionId),
    queryFn: () => getPaymentTransaction(transactionId),
    enabled: Boolean(transactionId),
  })
}

export function useInitiatePayment() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (payload: PaymentInitiationRequest) => initiatePayment(payload),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: billingQueryKeys.transactions(),
      })
    },
  })
}

export function useSynchronizePaymentStatus() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (transactionId: string) =>
      synchronizePaymentStatus(transactionId),

    onSuccess: (transaction) => {
      queryClient.setQueryData(
        billingQueryKeys.transaction(transaction.id),
        transaction,
      )

      queryClient.invalidateQueries({
        queryKey: billingQueryKeys.transactions(),
      })
    },
  })
}
