import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { toast } from 'sonner'

import AuthLayout from '@/features/auth/components/AuthLayout'
import GoogleAuthButton from '@/features/auth/components/GoogleAuthButton'
import { PasswordInput } from '@/features/auth/components/PasswordInput'
import {
  registerSchema,
  type RegisterFormValues,
} from '@/features/auth/schemas/auth_schemas'
import { useAuth } from '@/features/auth/hooks/use_auth'
import { getApiErrorMessage } from '@/utils/api_error'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

function Register() {
  const navigate = useNavigate()
  const { register: registerUser } = useAuth()
  const [isSubmitting, setIsSubmitting] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterFormValues>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      email: '',
      full_name: '',
      password: '',
      confirm_password: '',
    },
  })

  const onSubmit = async (values: RegisterFormValues) => {
    setIsSubmitting(true)

    try {
      await registerUser({
        email: values.email,
        full_name: values.full_name,
        password: values.password,
      })

      toast.success(
        'Account created successfully. Please check your email to verify your account.',
      )

      navigate('/login', { replace: true })
    } catch (error) {
      toast.error(getApiErrorMessage(error))
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <AuthLayout
      title="Create your account"
      description="Get started with your AI-powered resume and cover letter workspace."
      footer={
        <p>
          Already have an account?{' '}
          <Link
            to="/login"
            className="font-medium text-primary hover:underline"
          >
            Sign in
          </Link>
        </p>
      }
    >
      <div className="space-y-6">
        <GoogleAuthButton />

        <div className="relative">
          <div className="absolute inset-0 flex items-center">
            <span className="w-full border-t" />
          </div>

          <div className="relative flex justify-center text-xs uppercase">
            <span className="bg-card px-2 text-muted-foreground">
              Or register with email
            </span>
          </div>
        </div>

        <form
          onSubmit={(event) => {
            void handleSubmit(onSubmit)(event)
          }}
          className="space-y-4"
        >
          <div className="space-y-2">
            <Label htmlFor="full_name">Full name</Label>

            <Input
              id="full_name"
              type="text"
              autoComplete="name"
              placeholder="John Doe"
              aria-invalid={Boolean(errors.full_name)}
              {...register('full_name')}
            />

            {errors.full_name && (
              <p className="text-sm text-destructive">
                {errors.full_name.message}
              </p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="email">Email address</Label>

            <Input
              id="email"
              type="email"
              autoComplete="email"
              placeholder="you@example.com"
              aria-invalid={Boolean(errors.email)}
              {...register('email')}
            />

            {errors.email && (
              <p className="text-sm text-destructive">{errors.email.message}</p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>

            <PasswordInput
              id="password"
              autoComplete="new-password"
              placeholder="Create a password"
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
            <Label htmlFor="confirm_password">Confirm password</Label>

            <PasswordInput
              id="confirm_password"
              autoComplete="new-password"
              placeholder="Confirm your password"
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
            {isSubmitting ? 'Creating account...' : 'Create account'}
          </Button>
        </form>
      </div>
    </AuthLayout>
  )
}

export default Register
