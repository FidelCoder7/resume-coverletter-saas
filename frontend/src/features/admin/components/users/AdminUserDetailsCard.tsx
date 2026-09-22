import {
  CalendarDays,
  CheckCircle2,
  Clock3,
  Mail,
  ShieldCheck,
  UserRound,
  XCircle,
} from 'lucide-react'

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import type { AdminUserDetail } from '@/features/admin/types'

interface AdminUserDetailsCardProps {
  user: AdminUserDetail
}

function formatDate(value: string | null) {
  if (!value) {
    return 'Never'
  }

  return new Date(value).toLocaleString()
}

function getStatusClass(status: AdminUserDetail['status']) {
  switch (status) {
    case 'active':
      return 'border-primary/30 bg-primary/5 text-primary'
    case 'suspended':
    case 'deleted':
      return 'border-destructive/30 bg-destructive/5 text-destructive'
    default:
      return 'border-muted-foreground/30 bg-muted text-muted-foreground'
  }
}

function AdminUserDetailsCard({ user }: AdminUserDetailsCardProps) {
  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <Card>
        <CardHeader>
          <CardTitle>Account Information</CardTitle>
        </CardHeader>

        <CardContent className="space-y-5">
          <div className="flex items-start gap-3">
            <UserRound className="mt-0.5 size-5 text-muted-foreground" />

            <div className="min-w-0">
              <p className="text-xs font-medium text-muted-foreground">
                Full name
              </p>

              <p className="mt-1 font-medium">{user.full_name}</p>
            </div>
          </div>

          <div className="flex items-start gap-3">
            <Mail className="mt-0.5 size-5 text-muted-foreground" />

            <div className="min-w-0">
              <p className="text-xs font-medium text-muted-foreground">
                Email address
              </p>

              <p className="mt-1 break-all font-medium">{user.email}</p>
            </div>
          </div>

          <div className="flex items-start gap-3">
            <ShieldCheck className="mt-0.5 size-5 text-muted-foreground" />

            <div>
              <p className="text-xs font-medium text-muted-foreground">Role</p>

              <p className="mt-1 font-medium capitalize">{user.role}</p>
            </div>
          </div>

          <div className="flex items-start gap-3">
            <ShieldCheck className="mt-0.5 size-5 text-muted-foreground" />

            <div>
              <p className="text-xs font-medium text-muted-foreground">
                Subscription plan
              </p>

              <p className="mt-1 font-medium capitalize">
                {user.subscription_plan}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Account Status</CardTitle>
        </CardHeader>

        <CardContent className="space-y-5">
          <div>
            <p className="text-xs font-medium text-muted-foreground">
              Current status
            </p>

            <div className="mt-2">
              <span
                className={`inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-xs font-medium capitalize ${getStatusClass(user.status)}`}
              >
                {user.status === 'active' ? (
                  <CheckCircle2 className="size-3.5" />
                ) : (
                  <Clock3 className="size-3.5" />
                )}
                {user.status}
              </span>
            </div>
          </div>

          <div className="flex items-start gap-3">
            {user.is_email_verified ? (
              <CheckCircle2 className="mt-0.5 size-5 text-primary" />
            ) : (
              <XCircle className="mt-0.5 size-5 text-muted-foreground" />
            )}

            <div>
              <p className="text-xs font-medium text-muted-foreground">
                Email verification
              </p>

              <p className="mt-1 font-medium">
                {user.is_email_verified ? 'Verified' : 'Not verified'}
              </p>
            </div>
          </div>

          <div className="flex items-start gap-3">
            <Clock3 className="mt-0.5 size-5 text-muted-foreground" />

            <div>
              <p className="text-xs font-medium text-muted-foreground">
                Last login
              </p>

              <p className="mt-1 font-medium">
                {formatDate(user.last_login_at)}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card className="lg:col-span-2">
        <CardHeader>
          <CardTitle>Account Timeline</CardTitle>
        </CardHeader>

        <CardContent className="grid gap-5 sm:grid-cols-3">
          <div className="flex items-start gap-3">
            <CalendarDays className="mt-0.5 size-5 text-muted-foreground" />

            <div>
              <p className="text-xs font-medium text-muted-foreground">
                Created
              </p>

              <p className="mt-1 text-sm font-medium">
                {formatDate(user.created_at)}
              </p>
            </div>
          </div>

          <div className="flex items-start gap-3">
            <CalendarDays className="mt-0.5 size-5 text-muted-foreground" />

            <div>
              <p className="text-xs font-medium text-muted-foreground">
                Last updated
              </p>

              <p className="mt-1 text-sm font-medium">
                {formatDate(user.updated_at)}
              </p>
            </div>
          </div>

          <div className="flex items-start gap-3">
            <CalendarDays className="mt-0.5 size-5 text-muted-foreground" />

            <div>
              <p className="text-xs font-medium text-muted-foreground">
                Deleted
              </p>

              <p className="mt-1 text-sm font-medium">
                {formatDate(user.deleted_at)}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default AdminUserDetailsCard
