import { ArrowRight, Bot, FileText, Mail, Sparkles, Target } from 'lucide-react'
import { Link } from 'react-router-dom'

import { useAuth } from '@/features/auth/hooks/use_auth'
import { buttonVariants } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'

function Dashboard() {
  const { user } = useAuth()

  const firstName = user?.full_name.split(' ')[0] ?? 'there'

  return (
    <div className="mx-auto w-full max-w-7xl space-y-8">
      <section>
        <p className="text-sm font-medium text-primary">Your workspace</p>

        <h2 className="mt-1 text-2xl font-semibold tracking-tight sm:text-3xl">
          Welcome back, {firstName}!
        </h2>

        <p className="mt-2 max-w-2xl text-muted-foreground">
          Build stronger resumes and cover letters, optimize your applications,
          and use AI-powered tools to improve your job search.
        </p>
      </section>

      <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <CardTitle className="text-sm font-medium">Resumes</CardTitle>

              <FileText className="size-5 text-muted-foreground" />
            </div>
          </CardHeader>

          <CardContent>
            <p className="text-2xl font-semibold">0</p>

            <p className="mt-1 text-xs text-muted-foreground">
              Resume management coming soon
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <CardTitle className="text-sm font-medium">
                Cover Letters
              </CardTitle>

              <Mail className="size-5 text-muted-foreground" />
            </div>
          </CardHeader>

          <CardContent>
            <p className="text-2xl font-semibold">0</p>

            <p className="mt-1 text-xs text-muted-foreground">
              Cover letter management coming soon
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <CardTitle className="text-sm font-medium">AI Usage</CardTitle>

              <Bot className="size-5 text-muted-foreground" />
            </div>
          </CardHeader>

          <CardContent>
            <p className="text-2xl font-semibold">--</p>

            <p className="mt-1 text-xs text-muted-foreground">
              Usage tracking will appear here
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <CardTitle className="text-sm font-medium">
                Subscription
              </CardTitle>

              <Sparkles className="size-5 text-primary" />
            </div>
          </CardHeader>

          <CardContent>
            <p className="text-2xl font-semibold capitalize">
              {user?.subscription_plan ?? 'free'}
            </p>

            <p className="mt-1 text-xs text-muted-foreground">
              Your current subscription plan
            </p>
          </CardContent>
        </Card>
      </section>

      <section>
        <div className="mb-4">
          <h3 className="text-lg font-semibold">Quick actions</h3>

          <p className="mt-1 text-sm text-muted-foreground">
            Get started with your next application.
          </p>
        </div>

        <div className="grid gap-4 md:grid-cols-3">
          <Card className="transition-shadow hover:shadow-md">
            <CardHeader>
              <FileText className="mb-2 size-6 text-primary" />

              <CardTitle>Create a Resume</CardTitle>

              <CardDescription>
                Build and manage a professional resume tailored to your career
                goals.
              </CardDescription>
            </CardHeader>

            <CardContent>
              <Link
                to="/resumes"
                className={buttonVariants({ variant: 'outline' })}
              >
                Get started
                <ArrowRight />
              </Link>
            </CardContent>
          </Card>

          <Card className="transition-shadow hover:shadow-md">
            <CardHeader>
              <Mail className="mb-2 size-6 text-primary" />

              <CardTitle>Create a Cover Letter</CardTitle>

              <CardDescription>
                Create personalized cover letters designed for the jobs you're
                applying to.
              </CardDescription>
            </CardHeader>

            <CardContent>
              <Link
                to="/cover-letters"
                className={buttonVariants({ variant: 'outline' })}
              >
                Get started
                <ArrowRight />
              </Link>
            </CardContent>
          </Card>

          <Card className="transition-shadow hover:shadow-md">
            <CardHeader>
              <Target className="mb-2 size-6 text-primary" />

              <CardTitle>Optimize Your Resume</CardTitle>

              <CardDescription>
                Improve your resume for applicant tracking systems and increase
                your chances of getting noticed.
              </CardDescription>
            </CardHeader>

            <CardContent>
              <Link
                to="/ats"
                className={buttonVariants({ variant: 'outline' })}
              >
                Get started
                <ArrowRight />
              </Link>
            </CardContent>
          </Card>
        </div>
      </section>

      <section>
        <Card>
          <CardHeader>
            <CardTitle>Ready to build your next application?</CardTitle>

            <CardDescription>
              Your workspace is ready. Choose an action above to get started
              with your resume and cover letter workflow.
            </CardDescription>
          </CardHeader>
        </Card>
      </section>
    </div>
  )
}

export default Dashboard
