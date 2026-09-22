import { useState } from 'react'
import {
  AlertTriangle,
  Ban,
  CheckCircle2,
  LoaderCircle,
  RotateCcw,
} from 'lucide-react'

import { buttonVariants } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Textarea } from '@/components/ui/textarea'
import {
  useReactivateAdminUser,
  useSuspendAdminUser,
} from '@/features/admin/hooks/use_admin_users'
import type { AdminUserDetail } from '@/features/admin/types'
import { getApiErrorMessage } from '@/utils/api_error'

type AdminUserAction = 'suspend' | 'reactivate' | null

interface AdminUserActionsProps {
  user: AdminUserDetail
}

function AdminUserActions({ user }: AdminUserActionsProps) {
  const [pendingAction, setPendingAction] = useState<AdminUserAction>(null)
  const [reason, setReason] = useState('')

  const suspendUser = useSuspendAdminUser()
  const reactivateUser = useReactivateAdminUser()

  const isMutating = suspendUser.isPending || reactivateUser.isPending
  const mutationError = suspendUser.error ?? reactivateUser.error

  const resetAction = () => {
    setPendingAction(null)
    setReason('')
  }

  const handleConfirm = async () => {
    if (!pendingAction || isMutating) {
      return
    }

    const payload = reason.trim() ? { reason: reason.trim() } : undefined

    try {
      if (pendingAction === 'suspend') {
        await suspendUser.mutateAsync({
          userId: user.id,
          payload,
        })
      } else {
        await reactivateUser.mutateAsync({
          userId: user.id,
          payload,
        })
      }

      resetAction()
    } catch {
      // The mutation error is rendered below.
    }
  }

  const handleCancel = () => {
    if (!isMutating) {
      resetAction()
    }
  }

  const canSuspend = user.status === 'active'
  const canReactivate = user.status === 'suspended'

  if (!canSuspend && !canReactivate) {
    return null
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Administrative Actions</CardTitle>
      </CardHeader>

      <CardContent className="space-y-4">
        {pendingAction === null ? (
          <div className="flex flex-col gap-3 sm:flex-row">
            {canSuspend ? (
              <button
                type="button"
                className={buttonVariants({
                  variant: 'destructive',
                })}
                onClick={() => setPendingAction('suspend')}
              >
                <Ban />
                Suspend User
              </button>
            ) : null}

            {canReactivate ? (
              <button
                type="button"
                className={buttonVariants({
                  variant: 'outline',
                })}
                onClick={() => setPendingAction('reactivate')}
              >
                <RotateCcw />
                Reactivate User
              </button>
            ) : null}
          </div>
        ) : (
          <div className="space-y-4 rounded-lg border border-border bg-muted/30 p-4">
            <div className="flex items-start gap-3">
              <AlertTriangle className="mt-0.5 size-5 shrink-0 text-destructive" />

              <div>
                <p className="font-medium">
                  {pendingAction === 'suspend'
                    ? 'Suspend this user?'
                    : 'Reactivate this user?'}
                </p>

                <p className="mt-1 text-sm text-muted-foreground">
                  {pendingAction === 'suspend'
                    ? 'The user will no longer be able to use the application while their account is suspended.'
                    : 'The user account will be returned to an active state.'}
                </p>
              </div>
            </div>

            <div className="space-y-2">
              <label
                htmlFor="admin-user-action-reason"
                className="text-sm font-medium"
              >
                Reason
                <span className="ml-1 font-normal text-muted-foreground">
                  (optional)
                </span>
              </label>

              <Textarea
                id="admin-user-action-reason"
                value={reason}
                onChange={(event) => setReason(event.target.value)}
                placeholder={
                  pendingAction === 'suspend'
                    ? 'Enter the reason for suspending this account...'
                    : 'Enter the reason for reactivating this account...'
                }
                maxLength={2000}
                disabled={isMutating}
                rows={4}
              />

              <p className="text-xs text-muted-foreground">
                {reason.length}/2000 characters
              </p>
            </div>

            {mutationError ? (
              <div
                role="alert"
                className="rounded-lg border border-destructive/30 bg-destructive/5 px-4 py-3"
              >
                <p className="text-sm text-destructive">
                  {getApiErrorMessage(mutationError)}
                </p>
              </div>
            ) : null}

            <div className="flex flex-col-reverse gap-2 sm:flex-row sm:justify-end">
              <button
                type="button"
                className={buttonVariants({
                  variant: 'ghost',
                })}
                onClick={handleCancel}
                disabled={isMutating}
              >
                Cancel
              </button>

              <button
                type="button"
                className={buttonVariants({
                  variant:
                    pendingAction === 'suspend' ? 'destructive' : 'default',
                })}
                onClick={handleConfirm}
                disabled={isMutating}
              >
                {isMutating ? (
                  <>
                    <LoaderCircle className="animate-spin" />
                    {pendingAction === 'suspend'
                      ? 'Suspending...'
                      : 'Reactivating...'}
                  </>
                ) : pendingAction === 'suspend' ? (
                  <>
                    <Ban />
                    Confirm Suspension
                  </>
                ) : (
                  <>
                    <CheckCircle2 />
                    Confirm Reactivation
                  </>
                )}
              </button>
            </div>
          </div>
        )}

        {pendingAction === null && mutationError ? (
          <div
            role="alert"
            className="rounded-lg border border-destructive/30 bg-destructive/5 px-4 py-3"
          >
            <p className="text-sm text-destructive">
              {getApiErrorMessage(mutationError)}
            </p>
          </div>
        ) : null}
      </CardContent>
    </Card>
  )
}

export default AdminUserActions
