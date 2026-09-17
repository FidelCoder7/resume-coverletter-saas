import {
  Bot,
  Clock3,
  FileInput,
  History,
  Loader2,
  RotateCcw,
  ScanSearch,
  User,
} from 'lucide-react'

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Button } from '@/components/ui/button'

import { useRestoreResumeVersion } from '@/features/resumes/hooks/use_resume_versions'
import { useResumeVersions } from '@/features/resumes/hooks/use_resume_versions'
import type {
  ResumeVersion,
  ResumeVersionSource,
} from '@/features/resumes/types'
import { getApiErrorMessage } from '@/utils/api_error'

interface VersionHistoryProps {
  resumeId: string
}

function VersionHistory({ resumeId }: VersionHistoryProps) {
  const {
    data: versions = [],
    isLoading,
    isError,
    error,
  } = useResumeVersions(resumeId)

  const restoreMutation = useRestoreResumeVersion()

  const handleRestore = (version: ResumeVersion) => {
    const confirmed = window.confirm(
      `Restore Version ${version.version_number}?\n\n` +
        'This will replace the current resume content with this version. ' +
        'Your current state will be preserved as a new version.',
    )

    if (!confirmed) {
      return
    }

    restoreMutation.mutate({
      resumeId,
      versionId: version.id,
    })
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex items-start gap-3">
          <div className="rounded-lg bg-primary/10 p-2 text-primary">
            <History className="size-5" />
          </div>

          <div>
            <CardTitle>Version History</CardTitle>

            <CardDescription>
              Previous snapshots of this resume are preserved here.
            </CardDescription>
          </div>
        </div>
      </CardHeader>

      <CardContent>
        {isLoading && <VersionHistorySkeleton />}

        {isError && (
          <div className="rounded-lg border border-destructive/20 bg-destructive/5 px-4 py-3">
            <p className="text-sm font-medium text-destructive">
              Unable to load version history.
            </p>

            <p className="mt-1 text-sm text-muted-foreground">
              {getApiErrorMessage(error)}
            </p>
          </div>
        )}

        {!isLoading && !isError && versions.length === 0 && (
          <div className="rounded-lg border bg-muted/30 px-4 py-6 text-center">
            <History className="mx-auto size-6 text-muted-foreground" />

            <p className="mt-3 text-sm font-medium">No versions found</p>

            <p className="mt-1 text-sm text-muted-foreground">
              Version history will appear here as changes are made to this
              resume.
            </p>
          </div>
        )}

        {!isLoading && !isError && versions.length > 0 && (
          <div className="space-y-4">
            {versions.map((version, index) => (
              <VersionHistoryItem
                key={version.id}
                version={version}
                isLatest={index === 0}
                isRestoring={
                  restoreMutation.isPending &&
                  restoreMutation.variables?.versionId === version.id
                }
                isAnyVersionRestoring={restoreMutation.isPending}
                onRestore={handleRestore}
              />
            ))}
          </div>
        )}

        {restoreMutation.isError && (
          <div className="mt-4 rounded-lg border border-destructive/20 bg-destructive/5 px-4 py-3">
            <p className="text-sm font-medium text-destructive">
              Unable to restore version.
            </p>

            <p className="mt-1 text-sm text-muted-foreground">
              {getApiErrorMessage(restoreMutation.error)}
            </p>
          </div>
        )}

        {restoreMutation.isSuccess && (
          <div className="mt-4 rounded-lg border border-primary/20 bg-primary/5 px-4 py-3">
            <p className="text-sm font-medium text-primary">
              Resume restored successfully.
            </p>

            <p className="mt-1 text-sm text-muted-foreground">
              The restored state has been saved as a new version.
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  )
}

interface VersionHistoryItemProps {
  version: ResumeVersion
  isLatest: boolean
  isRestoring: boolean
  isAnyVersionRestoring: boolean
  onRestore: (version: ResumeVersion) => void
}

function VersionHistoryItem({
  version,
  isLatest,
  isRestoring,
  isAnyVersionRestoring,
  onRestore,
}: VersionHistoryItemProps) {
  return (
    <div className="relative flex gap-4">
      <div className="flex shrink-0 flex-col items-center">
        <div
          className={`flex size-9 items-center justify-center rounded-full border ${
            isLatest
              ? 'border-primary/30 bg-primary/10 text-primary'
              : 'bg-muted text-muted-foreground'
          }`}
        >
          {getSourceIcon(version.source)}
        </div>

        <div className="mt-2 h-full w-px bg-border last:hidden" />
      </div>

      <div className="min-w-0 flex-1 rounded-lg border p-4">
        <div className="flex flex-col gap-4">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
            <div className="min-w-0">
              <div className="flex flex-wrap items-center gap-2">
                <p className="font-medium">Version {version.version_number}</p>

                {isLatest && (
                  <span className="rounded-full bg-primary/10 px-2 py-0.5 text-xs font-medium text-primary">
                    Latest
                  </span>
                )}

                <VersionSourceBadge source={version.source} />
              </div>

              <p className="mt-1 text-sm text-muted-foreground">
                {version.change_summary || 'No change summary provided.'}
              </p>
            </div>

            <div className="flex shrink-0 items-center gap-1.5 text-xs text-muted-foreground">
              <Clock3 className="size-3.5" />

              <time dateTime={version.created_at}>
                {formatVersionDate(version.created_at)}
              </time>
            </div>
          </div>

          {!isLatest && (
            <div>
              <Button
                variant="outline"
                size="sm"
                disabled={isAnyVersionRestoring}
                onClick={() => onRestore(version)}
              >
                {isRestoring ? (
                  <>
                    <Loader2 className="animate-spin" />
                    Restoring...
                  </>
                ) : (
                  <>
                    <RotateCcw />
                    Restore
                  </>
                )}
              </Button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

function VersionSourceBadge({ source }: { source: ResumeVersionSource }) {
  return (
    <span className="rounded-full border bg-muted/30 px-2 py-0.5 text-xs font-medium text-muted-foreground">
      {formatVersionSource(source)}
    </span>
  )
}

function getSourceIcon(source: ResumeVersionSource) {
  switch (source) {
    case 'ai':
      return <Bot className="size-4" />

    case 'ats':
      return <ScanSearch className="size-4" />

    case 'restore':
      return <RotateCcw className="size-4" />

    case 'import':
      return <FileInput className="size-4" />

    case 'user':
    default:
      return <User className="size-4" />
  }
}

function formatVersionSource(source: ResumeVersionSource) {
  switch (source) {
    case 'ai':
      return 'AI'

    case 'ats':
      return 'ATS'

    case 'restore':
      return 'Restore'

    case 'import':
      return 'Import'

    case 'user':
      return 'User'
  }
}

function formatVersionDate(value: string) {
  return new Date(value).toLocaleString()
}

function VersionHistorySkeleton() {
  return (
    <div className="space-y-4">
      {Array.from({ length: 3 }).map((_, index) => (
        <div key={index} className="flex gap-4">
          <div className="size-9 shrink-0 animate-pulse rounded-full bg-muted" />

          <div className="flex-1 rounded-lg border p-4">
            <div className="space-y-3">
              <div className="h-4 w-40 animate-pulse rounded bg-muted" />

              <div className="h-4 w-3/4 animate-pulse rounded bg-muted" />

              <div className="h-3 w-32 animate-pulse rounded bg-muted" />
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

export default VersionHistory
