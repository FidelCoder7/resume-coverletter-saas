import { BarChart3, FileText, SearchCheck, Sparkles } from 'lucide-react'
import { Link } from 'react-router-dom'

import { buttonVariants } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'

function AIWorkspace() {
  return (
    <div className="mx-auto w-full max-w-7xl space-y-8">
      <section>
        <p className="text-sm font-medium text-primary">AI Workspace</p>

        <h1 className="mt-1 text-3xl font-semibold tracking-tight sm:text-4xl">
          Build a stronger job application with AI
        </h1>

        <p className="mt-3 max-w-3xl text-sm leading-6 text-muted-foreground">
          Generate tailored resume content, create targeted cover letters,
          optimize your resume for ATS systems, and review your AI usage.
        </p>
      </section>

      <section className="grid gap-4 md:grid-cols-2">
        <AIToolCard
          icon={FileText}
          title="AI Resume Generation"
          description="Generate tailored resume content based on your existing resume and target job."
          href="/ai/resume"
          action="Generate Resume"
        />

        <AIToolCard
          icon={Sparkles}
          title="AI Cover Letter"
          description="Create a targeted cover letter using your resume and a specific job description."
          href="/ai/cover-letter"
          action="Create Cover Letter"
        />

        <AIToolCard
          icon={SearchCheck}
          title="ATS Optimization"
          description="Analyze your resume against a job description and identify keywords and improvements."
          href="/ai/ats"
          action="Optimize Resume"
        />

        <AIToolCard
          icon={BarChart3}
          title="AI Usage History"
          description="Review your AI requests, usage statistics, token consumption, and feature breakdown."
          href="/ai/usage"
          action="View Usage"
        />
      </section>

      <Card>
        <CardHeader>
          <CardTitle>AI Workflow</CardTitle>

          <CardDescription>
            A practical workflow for preparing a targeted application.
          </CardDescription>
        </CardHeader>

        <CardContent>
          <div className="grid gap-6 md:grid-cols-4">
            <WorkflowStep
              number="01"
              title="Choose a resume"
              description="Start with the resume containing your current professional information."
            />

            <WorkflowStep
              number="02"
              title="Generate"
              description="Use AI to tailor your resume or create a cover letter."
            />

            <WorkflowStep
              number="03"
              title="Optimize"
              description="Run an ATS analysis against the target job description."
            />

            <WorkflowStep
              number="04"
              title="Review"
              description="Review the generated content before using it in an application."
            />
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

interface AIToolCardProps {
  icon: typeof FileText
  title: string
  description: string
  href: string
  action: string
}

function AIToolCard({
  icon: Icon,
  title,
  description,
  href,
  action,
}: AIToolCardProps) {
  return (
    <Card className="transition-shadow hover:shadow-md">
      <CardHeader>
        <Icon className="mb-2 size-6 text-primary" />

        <CardTitle>{title}</CardTitle>

        <CardDescription>{description}</CardDescription>
      </CardHeader>

      <CardContent>
        <Link
          to={href}
          className={buttonVariants({
            variant: 'outline',
          })}
        >
          {action}
        </Link>
      </CardContent>
    </Card>
  )
}

interface WorkflowStepProps {
  number: string
  title: string
  description: string
}

function WorkflowStep({ number, title, description }: WorkflowStepProps) {
  return (
    <div className="space-y-3">
      <span className="text-xs font-semibold text-primary">{number}</span>

      <div>
        <h3 className="font-medium">{title}</h3>

        <p className="mt-1 text-sm leading-6 text-muted-foreground">
          {description}
        </p>
      </div>
    </div>
  )
}

export default AIWorkspace
