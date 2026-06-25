"use client"

import { useEffect, useState } from "react"
import { checkHealth } from "@/lib/api"

type Status = "checking" | "online" | "offline"

export function ApiStatusBadge() {
  const [status, setStatus] = useState<Status>("checking")

  useEffect(() => {
    let active = true
    const run = async () => {
      const ok = await checkHealth()
      if (active) setStatus(ok ? "online" : "offline")
    }
    run()
    const id = setInterval(run, 30000)
    return () => {
      active = false
      clearInterval(id)
    }
  }, [])

  const config = {
    checking: { label: "Verificando", dot: "bg-muted-foreground/50" },
    online: { label: "API online", dot: "bg-emerald-600" },
    offline: { label: "API offline", dot: "bg-destructive" },
  }[status]

  return (
    <span className="inline-flex items-center gap-1.5 text-xs text-muted-foreground">
      <span
        className={`size-1.5 rounded-full ${config.dot}`}
        aria-hidden="true"
      />
      {config.label}
    </span>
  )
}
