import type { LucideIcon } from 'lucide-react'

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

interface AdminMetricCardProps {
  title: string
  value: string | number
  description: string
  icon: LucideIcon
  isLoading?: boolean
}

function AdminMetricCard({
  title,
  value,
  description,
  icon: Icon,
  isLoading = false,
}: AdminMetricCardProps) {
  return (
    <Card>
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between gap-3">
          <CardTitle className="text-sm font-medium">{title}</CardTitle>

          <div className="flex size-9 shrink-0 items-center justify-center rounded-lg bg-primary/10 text-primary">
            <Icon className="size-5" />
          </div>
        </div>
      </CardHeader>

      <CardContent>
        {isLoading ? (
          <div
            className="h-8 w-20 animate-pulse rounded-md bg-muted"
            aria-label={`Loading ${title}`}
          />
        ) : (
          <p className="text-2xl font-semibold tracking-tight">{value}</p>
        )}

        <p className="mt-1 text-xs text-muted-foreground">{description}</p>
      </CardContent>
    </Card>
  )
}

export default AdminMetricCard
