import { FileText, Pencil, Plus, Trash2 } from 'lucide-react'
import { Link, useNavigate } from 'react-router-dom'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import {
  useDeleteResume,
  useResumes,
} from '@/features/resumes/hooks/use_resumes'
import { getApiErrorMessage } from '@/utils/api_error'
import { Button, buttonVariants } from '@/components/ui/button'

function ResumeDashboard() {
  const navigate = useNavigate()

  const { data: resumes = [], isLoading, isError, error } = useResumes()

  const deleteMutation = useDeleteResume()

  function handleDelete(resumeId: string, title: string) {
    const confirmed = window.confirm(
      `Are you sure you want to delete "${title}"? This action cannot be undone.`,
    )

    if (!confirmed) {
      return
    }

    deleteMutation.mutate(resumeId)
  }

  if (isLoading) {
    return (
      <div className="mx-auto w-full max-w-7xl space-y-6">
        <div>
          <h2 className="text-2xl font-semibold tracking-tight sm:text-3xl">
            Resumes
          </h2>

          <p className="mt-2 text-muted-foreground">
            Create and manage your professional resumes.
          </p>
        </div>

        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {[1, 2, 3].map((item) => (
            <Card key={item}>
              <CardHeader>
                <div className="h-5 w-2/3 animate-pulse rounded bg-muted" />
                <div className="h-4 w-full animate-pulse rounded bg-muted" />
              </CardHeader>

              <CardContent>
                <div className="h-8 w-24 animate-pulse rounded bg-muted" />
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    )
  }

  if (isError) {
    return (
      <div className="mx-auto w-full max-w-7xl">
        <Card>
          <CardHeader>
            <CardTitle>Unable to load resumes</CardTitle>

            <CardDescription>{getApiErrorMessage(error)}</CardDescription>
          </CardHeader>

          <CardContent>
            <Button variant="outline" onClick={() => window.location.reload()}>
              Try again
            </Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="mx-auto w-full max-w-7xl space-y-8">
      <section className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p className="text-sm font-medium text-primary">Resume workspace</p>

          <h2 className="mt-1 text-2xl font-semibold tracking-tight sm:text-3xl">
            Your Resumes
          </h2>

          <p className="mt-2 text-muted-foreground">
            Create and manage professional resumes for your job applications.
          </p>
        </div>

        <Button onClick={() => navigate('/resumes/new')}>
          <Plus />
          Create Resume
        </Button>
      </section>

      {resumes.length === 0 ? (
        <Card>
          <CardHeader className="items-center text-center">
            <FileText className="size-10 text-muted-foreground" />

            <CardTitle>No resumes yet</CardTitle>

            <CardDescription className="max-w-md">
              Create your first resume to start building your professional
              profile and managing your career information.
            </CardDescription>
          </CardHeader>

          <CardContent className="flex justify-center">
            <Button onClick={() => navigate('/resumes/new')}>
              <Plus />
              Create your first resume
            </Button>
          </CardContent>
        </Card>
      ) : (
        <section className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {resumes.map((resume) => (
            <Card key={resume.id} className="transition-shadow hover:shadow-md">
              <CardHeader>
                <div className="flex items-start justify-between gap-4">
                  <div className="min-w-0">
                    <CardTitle className="truncate">{resume.title}</CardTitle>

                    <CardDescription className="mt-1">
                      Updated {new Date(resume.updated_at).toLocaleDateString()}
                    </CardDescription>
                  </div>

                  {resume.is_default && (
                    <span className="rounded-full bg-primary/10 px-2 py-1 text-xs font-medium text-primary">
                      Default
                    </span>
                  )}
                </div>
              </CardHeader>

              <CardContent className="space-y-4">
                <p className="line-clamp-3 min-h-15 text-sm text-muted-foreground">
                  {resume.summary || 'No summary added yet.'}
                </p>

                <div className="flex flex-wrap gap-2">
                  <Button
                    variant="default"
                    size="sm"
                    onClick={() => navigate(`/resumes/${resume.id}/edit`)}
                  >
                    <Pencil />
                    Edit
                  </Button>

                  <Link
                    to={`/resumes/${resume.id}`}
                    className={buttonVariants({ variant: 'outline' })}
                  >
                    Manage
                  </Link>

                  <Button
                    variant="destructive"
                    size="sm"
                    disabled={deleteMutation.isPending}
                    onClick={() => handleDelete(resume.id, resume.title)}
                  >
                    <Trash2 />
                    Delete
                  </Button>
                </div>

                {deleteMutation.isError &&
                  deleteMutation.variables === resume.id && (
                    <p className="text-sm text-destructive">
                      {getApiErrorMessage(deleteMutation.error)}
                    </p>
                  )}
              </CardContent>
            </Card>
          ))}
        </section>
      )}
    </div>
  )
}

export default ResumeDashboard
