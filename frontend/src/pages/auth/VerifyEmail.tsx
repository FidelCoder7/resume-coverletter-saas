import { useEffect, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { toast } from 'sonner'

import { verifyEmail } from '@/features/auth/api/auth_api'
import AuthLayout from '@/features/auth/components/AuthLayout'
import { getApiErrorMessage } from '@/utils/api_error'

function VerifyEmail() {
  const [searchParams] = useSearchParams()
  const token = searchParams.get('token')

  const [isVerified, setIsVerified] = useState(false)
  const [isVerifying, setIsVerifying] = useState(Boolean(token))

  useEffect(() => {
    if (!token) {
      return
    }

    const verify = async () => {
      try {
        await verifyEmail({ token })

        setIsVerified(true)

        toast.success('Your email address has been verified successfully.')
      } catch (error) {
        toast.error(getApiErrorMessage(error))
      } finally {
        setIsVerifying(false)
      }
    }

    void verify()
  }, [token])

  return (
    <AuthLayout
      title="Email verification"
      description="Verify your email address to activate your account."
    >
      <div className="space-y-4 text-center">
        {isVerifying && (
          <p className="text-sm text-muted-foreground">
            Verifying your email address...
          </p>
        )}

        {!isVerifying && isVerified && (
          <>
            <p className="text-sm text-muted-foreground">
              Your email address has been verified. You can now sign in to your
              account.
            </p>

            <Link
              to="/login"
              className="inline-flex h-8 items-center justify-center rounded-lg border border-border bg-background px-2.5 text-sm font-medium transition-colors hover:bg-muted hover:text-foreground"
            >
              Continue to sign in
            </Link>
          </>
        )}

        {!isVerifying && !isVerified && (
          <>
            <p className="text-sm text-destructive">
              We couldn't verify your email address. The link may be invalid or
              expired.
            </p>

            <Link
              to="/login"
              className="inline-flex h-8 items-center justify-center rounded-lg border border-border bg-background px-2.5 text-sm font-medium transition-colors hover:bg-muted hover:text-foreground"
            >
              Return to sign in
            </Link>
          </>
        )}

        {!token && (
          <p className="text-sm text-muted-foreground">
            No verification token was provided.
          </p>
        )}
      </div>
    </AuthLayout>
  )
}

export default VerifyEmail
