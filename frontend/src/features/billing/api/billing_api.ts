import apiClient from '@/api/axios'
import { API_ENDPOINTS } from '@/api/endpoint'

import type {
  PaymentInitiationRequest,
  PaymentInitiationResponse,
  PaymentStatusResponse,
  PaymentTransaction,
  PaymentTransactionListResponse,
  PaymentStatus,
} from '@/features/billing/types'

export async function initiatePayment(
  payload: PaymentInitiationRequest,
): Promise<PaymentInitiationResponse> {
  const response = await apiClient.post<PaymentInitiationResponse>(
    API_ENDPOINTS.BILLING.PAYMENTS,
    payload,
  )

  return response.data
}

export async function listPaymentTransactions(
  status?: PaymentStatus,
): Promise<PaymentTransaction[]> {
  const response = await apiClient.get<PaymentTransactionListResponse>(
    API_ENDPOINTS.BILLING.TRANSACTIONS,
    {
      params: status ? { status } : undefined,
    },
  )

  return response.data.transactions
}

export async function getPaymentTransaction(
  transactionId: string,
): Promise<PaymentTransaction> {
  const response = await apiClient.get<PaymentTransaction>(
    API_ENDPOINTS.BILLING.TRANSACTION_BY_ID(transactionId),
  )

  return response.data
}

export async function synchronizePaymentStatus(
  transactionId: string,
): Promise<PaymentTransaction> {
  const response = await apiClient.get<PaymentStatusResponse>(
    API_ENDPOINTS.BILLING.TRANSACTION_STATUS(transactionId),
  )

  return response.data.transaction
}
