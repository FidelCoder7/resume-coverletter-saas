import { useState } from 'react'
import { Link, useNavigate, useSearchParams } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { toast } from 'sonner'

import AuthLayout from '@/features/auth/components/AuthLayout'
import { PasswordInput } from '@/features/auth/components/PasswordInput'
import {
  resetPasswordSchema,
  type ResetPasswordFormValues,
} from '@/features/auth/schemas/auth_schemas'
import { resetPassword } from '@/features/auth/api/auth_api'
import { getApiErrorMessage } from '@/utils/api_error'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'

function ResetPassword() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()

  const token = searchParams.get('token')

  const [isSubmitting, setIsSubmitting] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ResetPasswordFormValues>({
    resolver: zodResolver(resetPasswordSchema),
    defaultValues: {
      password: '',
      confirm_password: '',
    },
  })

  const onSubmit = async (values: ResetPasswordFormValues) => {
    if (!token) {
      toast.error('Invalid or missing password reset token.')
      return
    }

    setIsSubmitting(true)

    try {
      await resetPassword({
        token,
        new_password: values.password,
      })

      toast.success('Your password has been reset successfully.')

      navigate('/login', { replace: true })
    } catch (error) {
      toast.error(getApiErrorMessage(error))
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <AuthLayout
      title="Reset your password"
      description="Choose a new password for your account."
      footer={
        <p>
          Remember your password?{' '}
          <Link
            to="/login"
            className="font-medium text-primary hover:underline"
          >
            Back to sign in
          </Link>
        </p>
      }
    >
      {!token ? (
        <div className="space-y-4 text-center">
          <p className="text-sm text-destructive">
            This password reset link is invalid or incomplete.
          </p>

          <Link
            to="/forgot-password"
            className="inline-flex h-8 items-center justify-center rounded-lg border border-border bg-background px-2.5 text-sm font-medium transition-colors hover:bg-muted hover:text-foreground"
          >
            Back to login
          </Link>
        </div>
      ) : (
        <form
          onSubmit={(event) => {
            void handleSubmit(onSubmit)(event)
          }}
          className="space-y-4"
        >
          <div className="space-y-2">
            <Label htmlFor="password">New password</Label>

            <PasswordInput
              id="password"
              autoComplete="new-password"
              placeholder="Enter your new password"
              aria-invalid={Boolean(errors.password)}
              {...register('password')}
            />

            {errors.password && (
              <p className="text-sm text-destructive">
                {errors.password.message}
              </p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="confirm_password">Confirm new password</Label>

            <PasswordInput
              id="confirm_password"
              autoComplete="new-password"
              placeholder="Confirm your new password"
              aria-invalid={Boolean(errors.confirm_password)}
              {...register('confirm_password')}
            />

            {errors.confirm_password && (
              <p className="text-sm text-destructive">
                {errors.confirm_password.message}
              </p>
            )}
          </div>

          <Button type="submit" className="w-full" disabled={isSubmitting}>
            {isSubmitting ? 'Resetting password...' : 'Reset password'}
          </Button>
        </form>
      )}
    </AuthLayout>
  )
}

export default ResetPassword
