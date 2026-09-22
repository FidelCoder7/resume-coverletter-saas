import { SlidersHorizontal, X } from 'lucide-react'

import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import type {
  AdminAuditAction,
  AdminAuditLogListParams,
} from '@/features/admin/types'

interface AdminAuditLogFiltersProps {
  filters: AdminAuditLogListParams
  onFiltersChange: (filters: AdminAuditLogListParams) => void
}

const actionLabels: Record<AdminAuditAction, string> = {
  user_suspended: 'User Suspended',
  user_activated: 'User Activated',
  user_deleted: 'User Deleted',
  user_restored: 'User Restored',
  user_role_changed: 'User Role Changed',
  user_subscription_changed: 'Subscription Changed',
}

function AdminAuditLogFilters({
  filters,
  onFiltersChange,
}: AdminAuditLogFiltersProps) {
  const hasActiveFilters =
    Boolean(filters.action) ||
    Boolean(filters.admin_id) ||
    Boolean(filters.target_user_id) ||
    Boolean(filters.created_after) ||
    Boolean(filters.created_before)

  function updateFilter<K extends keyof AdminAuditLogListParams>(
    key: K,
    value: AdminAuditLogListParams[K],
  ) {
    onFiltersChange({
      ...filters,
      page: 1,
      [key]: value,
    })
  }

  function handleActionChange(value: string) {
    updateFilter('action', value ? (value as AdminAuditAction) : undefined)
  }

  function handleAdminIdChange(value: string) {
    updateFilter('admin_id', value || undefined)
  }

  function handleTargetUserIdChange(value: string) {
    updateFilter('target_user_id', value || undefined)
  }

  function handleCreatedAfterChange(value: string) {
    updateFilter(
      'created_after',
      value ? new Date(value).toISOString() : undefined,
    )
  }

  function handleCreatedBeforeChange(value: string) {
    updateFilter(
      'created_before',
      value ? new Date(value).toISOString() : undefined,
    )
  }

  function clearFilters() {
    onFiltersChange({
      page: 1,
      page_size: filters.page_size,
    })
  }

  function formatDateTimeInputValue(value?: string) {
    if (!value) {
      return ''
    }

    const date = new Date(value)

    if (Number.isNaN(date.getTime())) {
      return ''
    }

    const timezoneOffset = date.getTimezoneOffset()
    const localDate = new Date(date.getTime() - timezoneOffset * 60 * 1000)

    return localDate.toISOString().slice(0, 16)
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        <SlidersHorizontal className="size-4 text-muted-foreground" />

        <div>
          <h3 className="text-sm font-medium">Audit log filters</h3>

          <p className="text-xs text-muted-foreground">
            Filter administrative activity by action, administrator, user, and
            date range.
          </p>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <div className="space-y-2">
          <Label htmlFor="admin-audit-action">Action</Label>

          <select
            id="admin-audit-action"
            value={filters.action ?? ''}
            onChange={(event) => handleActionChange(event.target.value)}
            className="h-8 w-full rounded-lg border border-input bg-background px-2.5 text-sm outline-none transition-colors focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/50"
          >
            <option value="">All actions</option>

            {Object.entries(actionLabels).map(([value, label]) => (
              <option key={value} value={value}>
                {label}
              </option>
            ))}
          </select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="admin-audit-admin-id">Admin ID</Label>

          <Input
            id="admin-audit-admin-id"
            value={filters.admin_id ?? ''}
            onChange={(event) => handleAdminIdChange(event.target.value)}
            placeholder="Administrator UUID"
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="admin-audit-target-user-id">Target User ID</Label>

          <Input
            id="admin-audit-target-user-id"
            value={filters.target_user_id ?? ''}
            onChange={(event) => handleTargetUserIdChange(event.target.value)}
            placeholder="User UUID"
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="admin-audit-created-after">Created After</Label>

          <Input
            id="admin-audit-created-after"
            type="datetime-local"
            value={formatDateTimeInputValue(filters.created_after)}
            onChange={(event) => handleCreatedAfterChange(event.target.value)}
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="admin-audit-created-before">Created Before</Label>

          <Input
            id="admin-audit-created-before"
            type="datetime-local"
            value={formatDateTimeInputValue(filters.created_before)}
            onChange={(event) => handleCreatedBeforeChange(event.target.value)}
          />
        </div>
      </div>

      {hasActiveFilters && (
        <div className="flex justify-end">
          <Button
            type="button"
            variant="ghost"
            size="sm"
            onClick={clearFilters}
          >
            <X />
            Clear filters
          </Button>
        </div>
      )}
    </div>
  )
}

export default AdminAuditLogFilters
