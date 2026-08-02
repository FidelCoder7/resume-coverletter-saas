import { Construction } from 'lucide-react'
import { Link } from 'react-router-dom'

import { Card, CardContent } from '@/components/ui/card'

interface ComingSoonProps {
  title: string
  description?: string
}

function ComingSoon({
  title,
  description = 'This feature is currently under development.',
}: ComingSoonProps) {
  return (
    <div className="flex min-h-[60vh] items-center justify-center">
      <Card className="w-full max-w-lg">
        <CardContent className="flex flex-col items-center px-6 py-12 text-center">
          <div className="mb-4 flex size-12 items-center justify-center rounded-full bg-primary/10 text-primary">
            <Construction className="size-6" />
          </div>

          <h2 className="text-xl font-semibold">{title}</h2>

          <p className="mt-2 max-w-md text-sm text-muted-foreground">
            {description}
          </p>

          <Link
            to="/dashboard"
            className="mt-6 inline-flex h-9 items-center justify-center rounded-lg bg-primary px-2.5 text-sm font-medium whitespace-nowrap text-primary-foreground transition-all outline-none hover:bg-primary/80 focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/50"
          >
            Return to Dashboard
          </Link>
        </CardContent>
      </Card>
    </div>
  )
}

export default ComingSoon
