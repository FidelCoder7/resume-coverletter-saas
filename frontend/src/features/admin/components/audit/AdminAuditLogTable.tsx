import {
  Activity,
  CheckCircle2,
  CircleAlert,
  Clock3,
  FileText,
  ShieldAlert,
} from 'lucide-react'

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import type { AdminAuditAction, AdminAuditLog } from '@/features/admin/types'

interface AdminAuditLogTableProps {
  logs: AdminAuditLog[]
}

const actionLabels: Record<AdminAuditAction, string> = {
  user_suspended: 'User Suspended',
  user_activated: 'User Activated',
  user_deleted: 'User Deleted',
  user_restored: 'User Restored',
  user_role_changed: 'User Role Changed',
  user_subscription_changed: 'Subscription Changed',
}

const actionClasses: Record<AdminAuditAction, string> = {
  user_suspended: 'border-destructive/30 bg-destructive/5 text-destructive',
  user_activated: 'border-primary/30 bg-primary/5 text-primary',
  user_deleted: 'border-destructive/30 bg-destructive/5 text-destructive',
  user_restored: 'border-primary/30 bg-primary/5 text-primary',
  user_role_changed:
    'border-muted-foreground/30 bg-muted text-muted-foreground',
  user_subscription_changed:
    'border-muted-foreground/30 bg-muted text-muted-foreground',
}

function formatDate(value: string) {
  return new Date(value).toLocaleString()
}

function AdminAuditActionIcon({ action }: { action: AdminAuditAction }) {
  if (action === 'user_suspended') {
    return <ShieldAlert className="size-3.5" />
  }

  if (action === 'user_activated' || action === 'user_restored') {
    return <CheckCircle2 className="size-3.5" />
  }

  if (action === 'user_deleted') {
    return <CircleAlert className="size-3.5" />
  }

  return <Activity className="size-3.5" />
}

function AdminAuditActionBadge({ action }: { action: AdminAuditAction }) {
  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-xs font-medium ${actionClasses[action]}`}
    >
      <AdminAuditActionIcon action={action} />
      {actionLabels[action]}
    </span>
  )
}

function AdminAuditLogTable({ logs }: AdminAuditLogTableProps) {
  if (logs.length === 0) {
    return (
      <Card>
        <CardContent className="flex min-h-56 flex-col items-center justify-center text-center">
          <FileText className="size-9 text-muted-foreground" />

          <h3 className="mt-3 text-sm font-semibold">No audit logs found</h3>

          <p className="mt-1 max-w-md text-sm text-muted-foreground">
            No administrative activity matches the current filter criteria.
          </p>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Administrative Activity</CardTitle>

        <CardDescription>
          Review administrative actions performed across the platform.
        </CardDescription>
      </CardHeader>

      <CardContent>
        <div className="overflow-x-auto">
          <table className="w-full min-w-[1080px] text-sm">
            <thead>
              <tr className="border-b text-left text-xs text-muted-foreground">
                <th className="px-3 py-3 font-medium">Timestamp</th>
                <th className="px-3 py-3 font-medium">Action</th>
                <th className="px-3 py-3 font-medium">Admin</th>
                <th className="px-3 py-3 font-medium">Target User</th>
                <th className="px-3 py-3 font-medium">Reason</th>
                <th className="px-3 py-3 font-medium">Metadata</th>
              </tr>
            </thead>

            <tbody className="divide-y">
              {logs.map((log) => (
                <tr
                  key={log.id}
                  className="transition-colors hover:bg-muted/50"
                >
                  <td className="whitespace-nowrap px-3 py-4 text-muted-foreground">
                    <div className="flex items-center gap-1.5">
                      <Clock3 className="size-3.5" />
                      {formatDate(log.created_at)}
                    </div>
                  </td>

                  <td className="px-3 py-4">
                    <AdminAuditActionBadge action={log.action} />
                  </td>

                  <td className="px-3 py-4">
                    <span
                      className="block max-w-[220px] truncate font-mono text-xs"
                      title={log.admin_id}
                    >
                      {log.admin_id}
                    </span>
                  </td>

                  <td className="px-3 py-4">
                    <span
                      className="block max-w-[220px] truncate font-mono text-xs"
                      title={log.target_user_id}
                    >
                      {log.target_user_id}
                    </span>
                  </td>

                  <td className="px-3 py-4">
                    <p
                      className="max-w-[280px] truncate text-muted-foreground"
                      title={log.reason ?? undefined}
                    >
                      {log.reason ?? 'No reason provided'}
                    </p>
                  </td>

                  <td className="px-3 py-4">
                    {log.event_metadata ? (
                      <span className="text-xs font-medium text-primary">
                        Available
                      </span>
                    ) : (
                      <span className="text-xs text-muted-foreground">
                        None
                      </span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </CardContent>
    </Card>
  )
}

export default AdminAuditLogTable
