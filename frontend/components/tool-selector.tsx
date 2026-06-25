"use client"

import { BarChart3, Check, Eraser, Replace } from "lucide-react"
import type { LucideIcon } from "lucide-react"
import type { ToolId } from "@/types"

interface ToolOption {
  id: ToolId
  title: string
  description: string
  icon: LucideIcon
}

const tools: ToolOption[] = [
  {
    id: "clean",
    title: "Limpar dados",
    description:
      "Remove linhas vazias, colunas vazias, duplicatas e padroniza nomes de colunas.",
    icon: Eraser,
  },
  {
    id: "convert",
    title: "Converter dados",
    description: "Exporta para JSON, Markdown ou SQL INSERT.",
    icon: Replace,
  },
  {
    id: "analyze",
    title: "Analisar planilha",
    description:
      "Mostra resumo, colunas, valores ausentes, duplicatas, categorias, datas e estatísticas.",
    icon: BarChart3,
  },
]

interface ToolSelectorProps {
  selected: ToolId
  onSelect: (id: ToolId) => void
  disabled?: boolean
}

export function ToolSelector({
  selected,
  onSelect,
  disabled,
}: ToolSelectorProps) {
  return (
    <div>
      <h2 className="text-sm font-medium text-foreground">
        O que você quer fazer?
      </h2>
      <p className="mt-1 text-xs text-muted-foreground">
        Escolha uma ferramenta para começar.
      </p>

      <div className="mt-4 flex flex-col gap-3">
        {tools.map((tool) => {
          const active = selected === tool.id
          const Icon = tool.icon
          return (
            <button
              key={tool.id}
              type="button"
              onClick={() => onSelect(tool.id)}
              disabled={disabled}
              aria-pressed={active}
              className={`flex items-start gap-3 rounded-lg border p-4 text-left transition-colors disabled:cursor-not-allowed disabled:opacity-50 ${
                active
                  ? "border-foreground/30 bg-secondary"
                  : "border-border bg-card hover:bg-secondary/40"
              }`}
            >
              <div
                className={`mt-0.5 flex size-8 shrink-0 items-center justify-center rounded-md border ${
                  active
                    ? "border-foreground/20 bg-background"
                    : "border-border bg-secondary"
                }`}
              >
                <Icon className="size-4 text-foreground" strokeWidth={1.5} />
              </div>
              <div className="min-w-0 flex-1">
                <div className="flex items-center justify-between gap-2">
                  <span className="text-sm font-medium">{tool.title}</span>
                  {active && (
                    <Check
                      className="size-4 shrink-0 text-foreground"
                      strokeWidth={1.5}
                    />
                  )}
                </div>
                <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
                  {tool.description}
                </p>
              </div>
            </button>
          )
        })}
      </div>
    </div>
  )
}
