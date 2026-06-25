"use client"

import { AlertCircle, Check, Loader2 } from "lucide-react"
import type { LucideIcon } from "lucide-react"

export function ErrorNote({ message }: { message: string }) {
  return (
    <div className="flex items-start gap-2 rounded-md border border-destructive/30 bg-destructive/5 px-3 py-2.5 text-sm text-destructive">
      <AlertCircle className="mt-0.5 size-4 shrink-0" strokeWidth={1.5} />
      <span>{message}</span>
    </div>
  )
}

export function SuccessNote({ message }: { message: string }) {
  return (
    <span className="inline-flex items-center gap-1.5 text-xs text-emerald-700">
      <Check className="size-3.5" strokeWidth={1.5} />
      {message}
    </span>
  )
}

interface ActionButtonProps {
  onClick: () => void
  loading?: boolean
  disabled?: boolean
  icon?: LucideIcon
  variant?: "primary" | "secondary"
  children: React.ReactNode
}

export function ActionButton({
  onClick,
  loading,
  disabled,
  icon: Icon,
  variant = "primary",
  children,
}: ActionButtonProps) {
  const base =
    "inline-flex items-center justify-center gap-2 rounded-md px-4 py-2 text-sm font-medium transition-colors disabled:cursor-not-allowed disabled:opacity-50"
  const styles =
    variant === "primary"
      ? "bg-primary text-primary-foreground hover:opacity-90"
      : "border border-border bg-background text-foreground hover:bg-secondary"

  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled || loading}
      className={`${base} ${styles}`}
    >
      {loading ? (
        <Loader2 className="size-4 animate-spin" strokeWidth={1.5} />
      ) : (
        Icon && <Icon className="size-4" strokeWidth={1.5} />
      )}
      {children}
    </button>
  )
}
