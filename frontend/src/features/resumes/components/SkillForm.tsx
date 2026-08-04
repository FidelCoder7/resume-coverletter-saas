import { zodResolver } from '@hookform/resolvers/zod'
import { Loader2 } from 'lucide-react'
import { useForm } from 'react-hook-form'

import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

import {
  skillSchema,
  type SkillFormValues,
} from '@/features/resumes/schemas/skill_schemas'

import type { Skill } from '@/features/resumes/types'
import { SKILL_LEVELS, type SkillLevel } from '@/types/resume'

interface SkillFormProps {
  skill?: Skill
  isSubmitting: boolean
  onSubmit: (values: SkillFormValues) => void
  onCancel: () => void
}

const skillLevelLabels: Record<SkillLevel, string> = {
  beginner: 'Beginner',
  intermediate: 'Intermediate',
  advanced: 'Advanced',
  expert: 'Expert',
}

function SkillForm({
  skill,
  isSubmitting,
  onSubmit,
  onCancel,
}: SkillFormProps) {
  const form = useForm<SkillFormValues>({
    resolver: zodResolver(skillSchema),
    defaultValues: {
      name: skill?.name ?? '',
      proficiency: skill?.proficiency ?? 'intermediate',
      display_order: skill?.display_order ?? 0,
    },
  })

  function handleSubmit(values: SkillFormValues) {
    onSubmit(values)
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>{skill ? 'Edit Skill' : 'Add Skill'}</CardTitle>
      </CardHeader>

      <CardContent>
        <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-6">
          <div className="grid gap-6 md:grid-cols-2">
            <div className="space-y-2">
              <Label htmlFor="name">Skill Name</Label>

              <Input
                id="name"
                {...form.register('name')}
                disabled={isSubmitting}
                placeholder="Python"
              />

              {form.formState.errors.name && (
                <p className="text-sm text-destructive">
                  {form.formState.errors.name.message}
                </p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="proficiency">Proficiency</Label>

              <select
                id="proficiency"
                {...form.register('proficiency')}
                disabled={isSubmitting}
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
              >
                {SKILL_LEVELS.map((level) => (
                  <option key={level} value={level}>
                    {skillLevelLabels[level]}
                  </option>
                ))}
              </select>

              {form.formState.errors.proficiency && (
                <p className="text-sm text-destructive">
                  {form.formState.errors.proficiency.message}
                </p>
              )}
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="display_order">Display Order</Label>

            <Input
              id="display_order"
              type="number"
              min={0}
              {...form.register('display_order', {
                valueAsNumber: true,
              })}
              disabled={isSubmitting}
            />

            {form.formState.errors.display_order && (
              <p className="text-sm text-destructive">
                {form.formState.errors.display_order.message}
              </p>
            )}
          </div>

          <div className="flex justify-end gap-3">
            <Button
              type="button"
              variant="outline"
              onClick={onCancel}
              disabled={isSubmitting}
            >
              Cancel
            </Button>

            <Button type="submit" disabled={isSubmitting}>
              {isSubmitting && <Loader2 className="animate-spin" />}

              {skill ? 'Save Changes' : 'Add Skill'}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  )
}

export default SkillForm
