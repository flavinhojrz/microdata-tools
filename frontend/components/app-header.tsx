import { Code2 } from "lucide-react"
import Link from "next/link"
import { ApiStatusBadge } from "@/components/api-status-badge"

const navLinks = [
  { label: "Ferramentas", href: "/#ferramentas" },
  { label: "Privacidade", href: "/privacy" },
  { label: "Apoiar", href: "/donate" },
]

export function AppHeader() {
  return (
    <header className="sticky top-0 z-30 border-b border-border bg-background/85 backdrop-blur-sm">
      <div className="mx-auto flex h-14 max-w-6xl items-center justify-between gap-4 px-5">
        <div className="flex items-baseline gap-2">
          <Link href="/" className="text-[15px] font-semibold tracking-tight">
            MicroData Tools
          </Link>
          <span className="hidden text-xs text-muted-foreground sm:inline">
            by MicroTechPro
          </span>
        </div>

        <nav className="hidden items-center gap-6 md:flex">
          {navLinks.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="text-sm text-muted-foreground transition-colors hover:text-foreground"
            >
              {link.label}
            </Link>
          ))}
        </nav>

        <div className="flex items-center gap-4">
          <div className="hidden sm:block">
            <ApiStatusBadge />
          </div>
          <a
            href="https://github.com/flavinhojrz/microdata-tools"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 rounded-md border border-border px-3 py-1.5 text-sm text-foreground transition-colors hover:bg-secondary"
          >
            <Code2 className="size-4" strokeWidth={1.5} />
            <span className="hidden sm:inline">GitHub</span>
          </a>
        </div>
      </div>
    </header>
  )
}
