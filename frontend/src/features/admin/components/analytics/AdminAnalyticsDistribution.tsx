import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'

export interface AdminAnalyticsDistributionItem {
  key: string
  label: string
  value: number
}

interface AdminAnalyticsDistributionProps {
  title: string
  description: string
  items: AdminAnalyticsDistributionItem[]
  isLoading?: boolean
}

function AdminAnalyticsDistribution({
  title,
  description,
  items,
  isLoading = false,
}: AdminAnalyticsDistributionProps) {
  const total = items.reduce((sum, item) => sum + item.value, 0)

  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>

        <CardDescription>{description}</CardDescription>
      </CardHeader>

      <CardContent>
        {isLoading ? (
          <div className="space-y-4">
            {Array.from({ length: 4 }).map((_, index) => (
              <div key={index}>
                <div className="flex items-center justify-between gap-4">
                  <div className="h-4 w-32 animate-pulse rounded bg-muted" />

                  <div className="h-4 w-12 animate-pulse rounded bg-muted" />
                </div>

                <div className="mt-2 h-2 animate-pulse rounded-full bg-muted" />
              </div>
            ))}
          </div>
        ) : items.length === 0 ? (
          <div className="flex min-h-32 items-center justify-center text-center">
            <p className="text-sm text-muted-foreground">
              No analytics data is available.
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {items.map((item) => {
              const percentage =
                total > 0 ? Math.min((item.value / total) * 100, 100) : 0

              return (
                <div key={item.key}>
                  <div className="flex items-center justify-between gap-4">
                    <span className="truncate text-sm font-medium">
                      {item.label}
                    </span>

                    <span className="shrink-0 text-sm text-muted-foreground">
                      {item.value.toLocaleString()}
                    </span>
                  </div>

                  <div className="mt-2 h-2 overflow-hidden rounded-full bg-muted">
                    <div
                      className="h-full rounded-full bg-primary transition-all"
                      style={{ width: `${percentage}%` }}
                    />
                  </div>

                  <p className="mt-1 text-xs text-muted-foreground">
                    {percentage.toFixed(1)}%
                  </p>
                </div>
              )
            })}
          </div>
        )}
      </CardContent>
    </Card>
  )
}

export default AdminAnalyticsDistribution
