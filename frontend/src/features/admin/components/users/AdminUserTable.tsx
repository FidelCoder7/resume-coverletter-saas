import {
  CheckCircle2,
  Clock3,
  Eye,
  ShieldCheck,
  UserRound,
  XCircle,
} from 'lucide-react'
import { Link } from 'react-router-dom'

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import type { AdminUserListItem } from '@/features/admin/types'

interface AdminUserTableProps {
  users: AdminUserListItem[]
}

const statusLabels: Record<AdminUserListItem['status'], string> = {
  pending: 'Pending',
  active: 'Active',
  suspended: 'Suspended',
  deleted: 'Deleted',
}

const statusClasses: Record<AdminUserListItem['status'], string> = {
  pending: 'border-muted-foreground/30 bg-muted text-muted-foreground',
  active: 'border-primary/30 bg-primary/5 text-primary',
  suspended: 'border-destructive/30 bg-destructive/5 text-destructive',
  deleted: 'border-destructive/30 bg-destructive/5 text-destructive',
}

function formatDate(value: string | null) {
  if (!value) {
    return 'Never'
  }

  return new Date(value).toLocaleString()
}

function AdminUserStatusBadge({
  status,
}: {
  status: AdminUserListItem['status']
}) {
  const Icon = status === 'active' ? CheckCircle2 : Clock3

  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-xs font-medium ${statusClasses[status]}`}
    >
      <Icon className="size-3.5" />
      {statusLabels[status]}
    </span>
  )
}

function AdminUserRoleBadge({ role }: { role: AdminUserListItem['role'] }) {
  const isAdmin = role === 'admin'
  const Icon = isAdmin ? ShieldCheck : UserRound

  return (
    <span className="inline-flex items-center gap-1.5 rounded-full border border-border bg-muted/50 px-2.5 py-1 text-xs font-medium capitalize">
      <Icon className="size-3.5" />
      {role}
    </span>
  )
}

function AdminUserVerificationStatus({ isVerified }: { isVerified: boolean }) {
  if (isVerified) {
    return (
      <span className="inline-flex items-center gap-1.5 text-xs font-medium text-primary">
        <CheckCircle2 className="size-4" />
        Verified
      </span>
    )
  }

  return (
    <span className="inline-flex items-center gap-1.5 text-xs font-medium text-muted-foreground">
      <XCircle className="size-4" />
      Unverified
    </span>
  )
}

function AdminUserTable({ users }: AdminUserTableProps) {
  if (users.length === 0) {
    return (
      <Card>
        <CardContent className="flex min-h-56 flex-col items-center justify-center text-center">
          <UserRound className="size-9 text-muted-foreground" />

          <h3 className="mt-3 text-sm font-semibold">No users found</h3>

          <p className="mt-1 max-w-md text-sm text-muted-foreground">
            No users match the current search and filter criteria.
          </p>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Users</CardTitle>

        <CardDescription>
          Manage platform users and inspect their account status.
        </CardDescription>
      </CardHeader>

      <CardContent>
        <div className="overflow-x-auto">
          <table className="w-full min-w-[1080px] text-sm">
            <thead>
              <tr className="border-b text-left text-xs text-muted-foreground">
                <th className="px-3 py-3 font-medium">User</th>
                <th className="px-3 py-3 font-medium">Role</th>
                <th className="px-3 py-3 font-medium">Plan</th>
                <th className="px-3 py-3 font-medium">Status</th>
                <th className="px-3 py-3 font-medium">Email</th>
                <th className="px-3 py-3 font-medium">Last Login</th>
                <th className="px-3 py-3 font-medium">Created</th>
                <th className="px-3 py-3 text-right font-medium">Action</th>
              </tr>
            </thead>

            <tbody className="divide-y">
              {users.map((user) => (
                <tr
                  key={user.id}
                  className="transition-colors hover:bg-muted/50"
                >
                  <td className="px-3 py-4">
                    <div className="max-w-[240px]">
                      <p className="truncate font-medium">{user.full_name}</p>

                      <p className="mt-1 truncate text-xs text-muted-foreground">
                        {user.email}
                      </p>
                    </div>
                  </td>

                  <td className="px-3 py-4">
                    <AdminUserRoleBadge role={user.role} />
                  </td>

                  <td className="px-3 py-4">
                    <span className="font-medium capitalize">
                      {user.subscription_plan}
                    </span>
                  </td>

                  <td className="px-3 py-4">
                    <AdminUserStatusBadge status={user.status} />
                  </td>

                  <td className="px-3 py-4">
                    <AdminUserVerificationStatus
                      isVerified={user.is_email_verified}
                    />
                  </td>

                  <td className="whitespace-nowrap px-3 py-4 text-muted-foreground">
                    {formatDate(user.last_login_at)}
                  </td>

                  <td className="whitespace-nowrap px-3 py-4 text-muted-foreground">
                    {formatDate(user.created_at)}
                  </td>

                  <td className="px-3 py-4 text-right">
                    <Link
                      to={`/admin/users/${user.id}`}
                      className="inline-flex items-center gap-1.5 text-sm font-medium text-primary hover:underline"
                    >
                      <Eye className="size-4" />
                      View
                    </Link>
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

export default AdminUserTable
