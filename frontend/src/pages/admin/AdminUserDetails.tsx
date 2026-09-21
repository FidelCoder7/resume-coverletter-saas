import { ArrowLeft, LoaderCircle } from 'lucide-react'
import { Link, useParams } from 'react-router-dom'

import { buttonVariants } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import AdminUserDetailsCard from '@/features/admin/components/users/AdminUserDetailsCard'
import { useAdminUser } from '@/features/admin/hooks/use_admin_users'
import { getApiErrorMessage } from '@/utils/api_error'
import AdminUserActions from '@/features/admin/components/users/AdminUserActions'

function AdminUserDetails() {
  const { userId } = useParams<{ userId: string }>()

  const { data: user, isLoading, isError, error } = useAdminUser(userId ?? '')

  return (
    <div className="mx-auto w-full max-w-7xl space-y-6">
      <section>
        <Link
          to="/admin/users"
          className={buttonVariants({
            variant: 'ghost',
            size: 'sm',
            className: '-ml-2',
          })}
        >
          <ArrowLeft />
          Back to users
        </Link>

        <div className="mt-4">
          <p className="text-sm font-medium text-primary">User account</p>

          <h2 className="mt-1 text-2xl font-semibold tracking-tight sm:text-3xl">
            User Details
          </h2>

          <p className="mt-2 max-w-2xl text-sm text-muted-foreground">
            Review account information, subscription status, verification,
            activity, and account timeline.
          </p>
        </div>
      </section>

      {isLoading ? (
        <Card>
          <CardContent className="flex min-h-56 items-center justify-center">
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <LoaderCircle className="size-4 animate-spin" />
              Loading user details...
            </div>
          </CardContent>
        </Card>
      ) : isError ? (
        <Card>
          <CardContent className="pt-6">
            <div className="rounded-lg border border-destructive/30 bg-destructive/5 px-4 py-3">
              <p className="text-sm text-destructive">
                {getApiErrorMessage(error)}
              </p>
            </div>
          </CardContent>
        </Card>
      ) : user ? (
        <>
          <section>
            <Card>
              <CardContent className="pt-6">
                <div className="flex flex-col gap-2">
                  <p className="text-lg font-semibold">{user.full_name}</p>

                  <p className="break-all text-sm text-muted-foreground">
                    {user.email}
                  </p>

                  <p className="font-mono text-xs text-muted-foreground">
                    {user.id}
                  </p>
                </div>
              </CardContent>
            </Card>
          </section>

          <AdminUserDetailsCard user={user} />

          <AdminUserActions user={user} />
        </>
      ) : (
        <Card>
          <CardContent className="flex min-h-56 flex-col items-center justify-center text-center">
            <p className="text-sm font-medium">User not found</p>

            <p className="mt-1 text-sm text-muted-foreground">
              The requested user account could not be found.
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

export default AdminUserDetails
