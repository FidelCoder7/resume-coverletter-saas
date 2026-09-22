import { Button } from '@/components/ui/button'

export type AdminAnalyticsPeriod = 7 | 30 | 90

interface AdminAnalyticsPeriodSelectorProps {
  value: AdminAnalyticsPeriod
  onChange: (value: AdminAnalyticsPeriod) => void
  disabled?: boolean
}

const periods: Array<{
  value: AdminAnalyticsPeriod
  label: string
}> = [
  {
    value: 7,
    label: '7 days',
  },
  {
    value: 30,
    label: '30 days',
  },
  {
    value: 90,
    label: '90 days',
  },
]

function AdminAnalyticsPeriodSelector({
  value,
  onChange,
  disabled = false,
}: AdminAnalyticsPeriodSelectorProps) {
  return (
    <div
      className="flex flex-wrap items-center gap-1 rounded-lg border bg-muted/30 p-1"
      aria-label="Analytics period"
    >
      {periods.map((period) => {
        const isActive = value === period.value

        return (
          <Button
            key={period.value}
            type="button"
            size="sm"
            variant={isActive ? 'secondary' : 'ghost'}
            aria-pressed={isActive}
            disabled={disabled}
            onClick={() => onChange(period.value)}
          >
            {period.label}
          </Button>
        )
      })}
    </div>
  )
}

export default AdminAnalyticsPeriodSelector
