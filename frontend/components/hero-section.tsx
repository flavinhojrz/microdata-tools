"use client"

import { ArrowDown, ArrowUpFromLine } from "lucide-react"

interface HeroSectionProps {
  onUploadClick: () => void
  onToolsClick: () => void
}

export function HeroSection({ onUploadClick, onToolsClick }: HeroSectionProps) {
  return (
    <section className="mx-auto max-w-6xl px-5 pt-16 pb-12 md:pt-24 md:pb-16">
      <div className="max-w-2xl">
        <p className="mb-4 text-sm text-muted-foreground">
          Ferramenta gratuita para dados do dia a dia
        </p>
        <h1 className="text-balance text-3xl font-semibold leading-tight tracking-tight md:text-[2.75rem] md:leading-[1.1]">
          Limpe, converta e analise planilhas em segundos.
        </h1>
        <p className="mt-5 max-w-xl text-pretty text-base leading-relaxed text-muted-foreground">
          Uma ferramenta gratuita para transformar arquivos CSV e Excel
          bagunçados em dados limpos, JSON, SQL, Markdown e relatórios simples.
        </p>

        <div className="mt-8 flex flex-wrap items-center gap-3">
          <button
            type="button"
            onClick={onUploadClick}
            className="inline-flex items-center gap-2 rounded-md bg-primary px-4 py-2.5 text-sm font-medium text-primary-foreground transition-opacity hover:opacity-90"
          >
            <ArrowUpFromLine className="size-4" strokeWidth={1.5} />
            Enviar planilha
          </button>
          <button
            type="button"
            onClick={onToolsClick}
            className="inline-flex items-center gap-2 rounded-md border border-border px-4 py-2.5 text-sm font-medium text-foreground transition-colors hover:bg-secondary"
          >
            <ArrowDown className="size-4" strokeWidth={1.5} />
            Ver ferramentas
          </button>
        </div>

        <p className="mt-6 text-sm text-muted-foreground">
          Sem login. Gratuito. Feito para dados do dia a dia.
        </p>
      </div>
    </section>
  )
}
