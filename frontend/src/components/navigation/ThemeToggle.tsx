import { Moon, Sun } from 'lucide-react'
import { useTheme } from 'next-themes'

import { Button } from '@/components/ui/button'

function ThemeToggle() {
  const { resolvedTheme, setTheme } = useTheme()

  const isDark = resolvedTheme === 'dark'

  const handleToggle = () => {
    setTheme(isDark ? 'light' : 'dark')
  }

  return (
    <Button
      type="button"
      variant="ghost"
      size="icon"
      aria-label={isDark ? 'Switch to light theme' : 'Switch to dark theme'}
      title={isDark ? 'Switch to light theme' : 'Switch to dark theme'}
      onClick={handleToggle}
    >
      {isDark ? <Sun /> : <Moon />}
    </Button>
  )
}

export default ThemeToggle
