import { Button } from '@/components/ui/button'
import { getGoogleLoginUrl } from '@/features/auth/api/auth_api'

function GoogleAuthButton() {
  const handleGoogleLogin = () => {
    window.location.assign(getGoogleLoginUrl())
  }

  return (
    <Button
      type="button"
      variant="outline"
      className="w-full"
      onClick={handleGoogleLogin}
    >
      <span
        aria-hidden="true"
        className="flex size-5 items-center justify-center text-sm font-bold"
      >
        G
      </span>
      Continue with Google
    </Button>
  )
}

export default GoogleAuthButton
