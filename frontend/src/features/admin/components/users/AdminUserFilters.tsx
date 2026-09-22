import { Search, SlidersHorizontal, X } from 'lucide-react'

import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import type { AdminUserListParams } from '@/features/admin/types'
import type { AccountStatus, SubscriptionPlan, UserRole } from '@/types/user'

interface AdminUserFiltersProps {
  filters: AdminUserListParams
  onFiltersChange: (filters: AdminUserListParams) => void
}

function AdminUserFilters({ filters, onFiltersChange }: AdminUserFiltersProps) {
  const hasActiveFilters =
    Boolean(filters.search) ||
    Boolean(filters.role) ||
    Boolean(filters.status) ||
    Boolean(filters.subscription_plan)

  function updateFilter<K extends keyof AdminUserListParams>(
    key: K,
    value: AdminUserListParams[K],
  ) {
    onFiltersChange({
      ...filters,
      page: 1,
      [key]: value,
    })
  }

  function handleSearchChange(value: string) {
    updateFilter('search', value || undefined)
  }

  function handleRoleChange(value: string) {
    updateFilter('role', value ? (value as UserRole) : undefined)
  }

  function handleStatusChange(value: string) {
    updateFilter('status', value ? (value as AccountStatus) : undefined)
  }

  function handlePlanChange(value: string) {
    updateFilter(
      'subscription_plan',
      value ? (value as SubscriptionPlan) : undefined,
    )
  }

  function clearFilters() {
    onFiltersChange({
      page: 1,
      page_size: filters.page_size,
    })
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        <SlidersHorizontal className="size-4 text-muted-foreground" />

        <div>
          <h3 className="text-sm font-medium">User filters</h3>

          <p className="text-xs text-muted-foreground">
            Search and filter administrative users.
          </p>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <div className="space-y-2">
          <Label htmlFor="admin-user-search">Search</Label>

          <div className="relative">
            <Search className="pointer-events-none absolute top-1/2 left-2.5 size-4 -translate-y-1/2 text-muted-foreground" />

            <Input
              id="admin-user-search"
              value={filters.search ?? ''}
              onChange={(event) => handleSearchChange(event.target.value)}
              placeholder="Name or email"
              className="pl-9"
            />
          </div>
        </div>

        <div className="space-y-2">
          <Label htmlFor="admin-user-role">Role</Label>

          <select
            id="admin-user-role"
            value={filters.role ?? ''}
            onChange={(event) => handleRoleChange(event.target.value)}
            className="h-8 w-full rounded-lg border border-input bg-background px-2.5 text-sm outline-none transition-colors focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/50"
          >
            <option value="">All roles</option>
            <option value="user">User</option>
            <option value="admin">Admin</option>
          </select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="admin-user-status">Status</Label>

          <select
            id="admin-user-status"
            value={filters.status ?? ''}
            onChange={(event) => handleStatusChange(event.target.value)}
            className="h-8 w-full rounded-lg border border-input bg-background px-2.5 text-sm outline-none transition-colors focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/50"
          >
            <option value="">All statuses</option>
            <option value="pending">Pending</option>
            <option value="active">Active</option>
            <option value="suspended">Suspended</option>
            <option value="deleted">Deleted</option>
          </select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="admin-user-plan">Subscription</Label>

          <select
            id="admin-user-plan"
            value={filters.subscription_plan ?? ''}
            onChange={(event) => handlePlanChange(event.target.value)}
            className="h-8 w-full rounded-lg border border-input bg-background px-2.5 text-sm outline-none transition-colors focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/50"
          >
            <option value="">All plans</option>
            <option value="free">Free</option>
            <option value="pro">Pro</option>
          </select>
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

export default AdminUserFilters
