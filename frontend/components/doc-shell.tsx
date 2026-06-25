import { ArrowLeft } from "lucide-react"
import Link from "next/link"
import { AppHeader } from "@/components/app-header"
import { Footer } from "@/components/footer"

interface DocShellProps {
  title: string
  intro: string
  /** Texto curto exibido abaixo da intro (ex.: data de atualização). */
  meta?: string
  children: React.ReactNode
}

export function DocShell({ title, intro, meta, children }: DocShellProps) {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <AppHeader />

      <main className="mx-auto max-w-3xl px-5 py-16">
        <Link
          href="/"
          className="inline-flex items-center gap-1.5 text-sm text-muted-foreground transition-colors hover:text-foreground"
        >
          <ArrowLeft className="size-4" strokeWidth={1.5} />
          Voltar
        </Link>

        <h1 className="mt-6 text-3xl font-semibold tracking-tight">{title}</h1>
        <p className="mt-4 text-pretty text-base leading-relaxed text-muted-foreground">
          {intro}
        </p>
        {meta && <p className="mt-2 text-sm text-muted-foreground">{meta}</p>}

        <div className="mt-10 flex flex-col gap-10">{children}</div>
      </main>

      <Footer />
    </div>
  )
}

interface DocSectionProps {
  title: string
  children: React.ReactNode
}

export function DocSection({ title, children }: DocSectionProps) {
  return (
    <section>
      <h2 className="text-lg font-semibold tracking-tight">{title}</h2>
      <div className="mt-3 flex flex-col gap-3 text-sm leading-relaxed text-muted-foreground">
        {children}
      </div>
    </section>
  )
}
