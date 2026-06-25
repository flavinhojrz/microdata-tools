import type { LucideIcon } from "lucide-react"

interface EmptyStateProps {
  icon: LucideIcon
  title: string
  description?: string
}

export function EmptyState({ icon: Icon, title, description }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center rounded-lg border border-dashed border-border bg-card px-6 py-14 text-center">
      <div className="mb-4 flex size-10 items-center justify-center rounded-full border border-border bg-background">
        <Icon className="size-4 text-muted-foreground" strokeWidth={1.5} />
      </div>
      <p className="text-sm font-medium text-foreground">{title}</p>
      {description && (
        <p className="mt-1 max-w-xs text-pretty text-xs leading-relaxed text-muted-foreground">
          {description}
        </p>
      )}
    </div>
  )
}
