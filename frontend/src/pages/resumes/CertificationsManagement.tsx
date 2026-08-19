import { Award, ExternalLink, Pencil, Plus, Trash2 } from 'lucide-react'
import { useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import { Button, buttonVariants } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'

import CertificationForm from '@/features/resumes/components/CertificationForm'

import {
  useCertifications,
  useCreateCertification,
  useDeleteCertification,
  useUpdateCertification,
} from '@/features/resumes/hooks/use_certifications'

import type { Certification } from '@/features/resumes/types'
import type { CertificationFormValues } from '@/features/resumes/schemas/certification_schemas'

import { getApiErrorMessage } from '@/utils/api_error'

function CertificationsManagement() {
  const { resumeId } = useParams<{
    resumeId: string
  }>()

  const [editingCertification, setEditingCertification] =
    useState<Certification | null>(null)

  const [isCreating, setIsCreating] = useState(false)

  const {
    data: certifications = [],
    isLoading,
    isError,
    error,
  } = useCertifications(resumeId ?? '')

  const createMutation = useCreateCertification()
  const updateMutation = useUpdateCertification()
  const deleteMutation = useDeleteCertification()

  if (!resumeId) {
    return (
      <div className="mx-auto w-full max-w-7xl">
        <Card>
          <CardHeader>
            <CardTitle>Resume not found</CardTitle>

            <CardDescription>
              The requested resume could not be identified.
            </CardDescription>
          </CardHeader>
        </Card>
      </div>
    )
  }

  const currentResumeId = resumeId

  function handleCreate(values: CertificationFormValues) {
    createMutation.mutate(
      {
        resumeId: currentResumeId,
        payload: {
          ...values,
          credential_id: values.credential_id || null,
          credential_url: values.credential_url || null,
          expiration_date: values.expiration_date || null,
        },
      },
      {
        onSuccess: () => {
          setIsCreating(false)
        },
      },
    )
  }

  function handleUpdate(values: CertificationFormValues) {
    if (!editingCertification) {
      return
    }

    updateMutation.mutate(
      {
        certificationId: editingCertification.id,
        resumeId: currentResumeId,
        payload: {
          ...values,
          credential_id: values.credential_id || null,
          credential_url: values.credential_url || null,
          expiration_date: values.expiration_date || null,
        },
      },
      {
        onSuccess: () => {
          setEditingCertification(null)
        },
      },
    )
  }

  function handleDelete(certification: Certification) {
    const confirmed = window.confirm(
      `Are you sure you want to delete "${certification.name}"? This action cannot be undone.`,
    )

    if (!confirmed) {
      return
    }

    deleteMutation.mutate({
      certificationId: certification.id,
      resumeId: currentResumeId,
    })
  }

  if (isLoading) {
    return (
      <div className="mx-auto w-full max-w-7xl space-y-6">
        <div className="h-8 w-64 animate-pulse rounded bg-muted" />

        <div className="grid gap-4">
          <div className="h-40 animate-pulse rounded-lg bg-muted" />

          <div className="h-40 animate-pulse rounded-lg bg-muted" />
        </div>
      </div>
    )
  }

  if (isError) {
    return (
      <div className="mx-auto w-full max-w-7xl">
        <Card>
          <CardHeader>
            <CardTitle>Unable to load certifications</CardTitle>

            <CardDescription>{getApiErrorMessage(error)}</CardDescription>
          </CardHeader>

          <CardContent>
            <Button onClick={() => window.location.reload()}>Try again</Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="mx-auto w-full max-w-7xl space-y-8">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <Link
            to={`/resumes/${resumeId}`}
            className={buttonVariants({
              variant: 'outline',
            })}
          >
            Back to Resume
          </Link>

          <h1 className="mt-6 text-2xl font-semibold tracking-tight sm:text-3xl">
            Certifications
          </h1>

          <p className="mt-2 text-muted-foreground">
            Showcase professional certifications, credentials, and industry
            qualifications.
          </p>
        </div>

        {!isCreating && !editingCertification && (
          <Button onClick={() => setIsCreating(true)}>
            <Plus />
            Add Certification
          </Button>
        )}
      </div>

      {(isCreating || editingCertification) && (
        <Card>
          <CardHeader>
            <CardTitle>
              {editingCertification
                ? 'Edit Certification'
                : 'Add Certification'}
            </CardTitle>

            <CardDescription>
              {editingCertification
                ? 'Update the certification information on your resume.'
                : 'Add a professional certification or credential to your resume.'}
            </CardDescription>
          </CardHeader>

          <CardContent>
            <CertificationForm
              certification={editingCertification ?? undefined}
              isSubmitting={
                createMutation.isPending || updateMutation.isPending
              }
              onSubmit={editingCertification ? handleUpdate : handleCreate}
              onCancel={() => {
                setIsCreating(false)
                setEditingCertification(null)
              }}
            />

            {(createMutation.isError || updateMutation.isError) && (
              <p className="mt-4 text-sm text-destructive">
                {getApiErrorMessage(
                  createMutation.error || updateMutation.error,
                )}
              </p>
            )}
          </CardContent>
        </Card>
      )}

      {deleteMutation.isError && (
        <Card>
          <CardContent className="pt-6">
            <p className="text-sm text-destructive">
              {getApiErrorMessage(deleteMutation.error)}
            </p>
          </CardContent>
        </Card>
      )}

      {certifications.length === 0 ? (
        <Card>
          <CardHeader>
            <CardTitle>No certifications yet</CardTitle>

            <CardDescription>
              Add your first certification to strengthen your professional
              profile.
            </CardDescription>
          </CardHeader>

          <CardContent>
            {!isCreating && (
              <Button onClick={() => setIsCreating(true)}>
                <Plus />
                Add Your First Certification
              </Button>
            )}
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-4">
          {certifications.map((certification) => (
            <Card key={certification.id}>
              <CardHeader>
                <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
                  <div className="min-w-0">
                    <div className="flex items-start gap-3">
                      <Award className="mt-1 size-5 shrink-0 text-primary" />

                      <div>
                        <CardTitle>{certification.name}</CardTitle>

                        <CardDescription className="mt-1">
                          {certification.issuing_organization}
                        </CardDescription>
                      </div>
                    </div>
                  </div>

                  <div className="flex shrink-0 gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => {
                        setEditingCertification(certification)
                        setIsCreating(false)
                      }}
                    >
                      <Pencil />
                      Edit
                    </Button>

                    <Button
                      variant="destructive"
                      size="sm"
                      disabled={
                        deleteMutation.isPending &&
                        deleteMutation.variables?.certificationId ===
                          certification.id
                      }
                      onClick={() => handleDelete(certification)}
                    >
                      <Trash2 />
                      {deleteMutation.isPending &&
                      deleteMutation.variables?.certificationId ===
                        certification.id
                        ? 'Deleting...'
                        : 'Delete'}
                    </Button>
                  </div>
                </div>
              </CardHeader>

              <CardContent className="space-y-4">
                <div className="flex flex-wrap gap-4 text-sm text-muted-foreground">
                  <span>
                    Issued{' '}
                    {new Date(certification.issue_date).toLocaleDateString()}
                  </span>

                  {certification.does_not_expire ? (
                    <span>Does not expire</span>
                  ) : (
                    certification.expiration_date && (
                      <span>
                        Expires{' '}
                        {new Date(
                          certification.expiration_date,
                        ).toLocaleDateString()}
                      </span>
                    )
                  )}
                </div>

                {certification.credential_id && (
                  <p className="text-sm text-muted-foreground">
                    <span className="font-medium text-foreground">
                      Credential ID:
                    </span>{' '}
                    {certification.credential_id}
                  </p>
                )}

                {certification.credential_url && (
                  <a
                    href={certification.credential_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className={buttonVariants({
                      variant: 'outline',
                      size: 'sm',
                    })}
                  >
                    <ExternalLink />
                    Verify Credential
                  </a>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}

export default CertificationsManagement
