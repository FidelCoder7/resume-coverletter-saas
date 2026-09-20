import type { PaymentStatus } from '@/features/billing/types'

interface PaymentStatusBadgeProps {
  status: PaymentStatus
}

const statusLabels: Record<PaymentStatus, string> = {
  pending: 'Pending',
  completed: 'Completed',
  failed: 'Failed',
  cancelled: 'Cancelled',
  expired: 'Expired',
}

const statusClasses: Record<PaymentStatus, string> = {
  pending: 'bg-muted text-muted-foreground',
  completed: 'bg-primary/10 text-primary',
  failed: 'bg-destructive/10 text-destructive',
  cancelled: 'bg-muted text-muted-foreground',
  expired: 'bg-muted text-muted-foreground',
}

function PaymentStatusBadge({ status }: PaymentStatusBadgeProps) {
  return (
    <span
      className={`inline-flex items-center rounded-full px-2.5 py-1 text-xs font-medium ${statusClasses[status]}`}
    >
      {statusLabels[status]}
    </span>
  )
}

export default PaymentStatusBadge
