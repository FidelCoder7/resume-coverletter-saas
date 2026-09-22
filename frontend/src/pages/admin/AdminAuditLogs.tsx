import { ChevronLeft, ChevronRight, LoaderCircle } from 'lucide-react'
import { useState } from 'react'

import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import AdminAuditLogFilters from '@/features/admin/components/audit/AdminAuditLogFilters'
import AdminAuditLogTable from '@/features/admin/components/audit/AdminAuditLogTable'
import { useAdminAuditLogs } from '@/features/admin/hooks/use_admin_audit_logs'
import type { AdminAuditLogListParams } from '@/features/admin/types'
import { getApiErrorMessage } from '@/utils/api_error'

const DEFAULT_PAGE_SIZE = 20

function AdminAuditLogs() {
  const [filters, setFilters] = useState<AdminAuditLogListParams>({
    page: 1,
    page_size: DEFAULT_PAGE_SIZE,
  })

  const { data, isLoading, isError, error, isFetching } =
    useAdminAuditLogs(filters)

  const currentPage = data?.page ?? filters.page ?? 1
  const totalPages = data?.total_pages ?? 1

  function goToPage(page: number) {
    if (page < 1 || page > totalPages || page === currentPage) {
      return
    }

    setFilters((current) => ({
      ...current,
      page,
    }))
  }

  return (
    <div className="mx-auto w-full max-w-7xl space-y-6">
      <section>
        <h2 className="text-2xl font-semibold tracking-tight sm:text-3xl">
          Audit Logs
        </h2>

        <p className="mt-2 max-w-2xl text-sm text-muted-foreground">
          Review administrative actions and activity across the platform.
        </p>
      </section>

      <Card>
        <CardContent className="pt-6">
          <AdminAuditLogFilters
            filters={filters}
            onFiltersChange={setFilters}
          />
        </CardContent>
      </Card>

      {isLoading ? (
        <Card>
          <CardContent className="flex min-h-56 items-center justify-center">
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <LoaderCircle className="size-4 animate-spin" />
              Loading audit logs...
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
      ) : (
        <>
          <div className="relative">
            <AdminAuditLogTable logs={data?.items ?? []} />

            {isFetching && (
              <div className="pointer-events-none absolute inset-x-0 top-0 flex justify-center">
                <div className="mt-2 inline-flex items-center gap-2 rounded-full border bg-background px-3 py-1.5 text-xs text-muted-foreground shadow-sm">
                  <LoaderCircle className="size-3.5 animate-spin" />
                  Updating...
                </div>
              </div>
            )}
          </div>

          {data && data.total > 0 && (
            <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <p className="text-sm text-muted-foreground">
                Showing{' '}
                <span className="font-medium text-foreground">
                  {(data.page - 1) * data.page_size + 1}
                </span>{' '}
                to{' '}
                <span className="font-medium text-foreground">
                  {Math.min(data.page * data.page_size, data.total)}
                </span>{' '}
                of{' '}
                <span className="font-medium text-foreground">
                  {data.total}
                </span>{' '}
                audit logs
              </p>

              <div className="flex items-center gap-2">
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={() => goToPage(currentPage - 1)}
                  disabled={currentPage <= 1 || isFetching}
                >
                  <ChevronLeft />
                  Previous
                </Button>

                <span className="px-2 text-sm text-muted-foreground">
                  Page {currentPage} of {totalPages}
                </span>

                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={() => goToPage(currentPage + 1)}
                  disabled={currentPage >= totalPages || isFetching}
                >
                  Next
                  <ChevronRight />
                </Button>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  )
}

export default AdminAuditLogs
