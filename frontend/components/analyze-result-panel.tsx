"use client"

import { useState } from "react"
import { BarChart3 } from "lucide-react"
import type { AnalyzePreviewResult } from "@/types"
import { analyzePreview, ApiError, type AnalyzeOptions } from "@/lib/api"
import { ActionButton, ErrorNote } from "@/components/panel-ui"

interface AnalyzeResultPanelProps {
  file: File
}

function Section({
  title,
  children,
}: {
  title: string
  children: React.ReactNode
}) {
  return (
    <div className="border-t border-border pt-5">
      <h4 className="mb-3 text-xs font-medium uppercase tracking-wide text-muted-foreground">
        {title}
      </h4>
      {children}
    </div>
  )
}

function num(value?: number | null) {
  if (value === undefined || value === null) return "—"
  return Number.isInteger(value)
    ? value.toLocaleString("pt-BR")
    : value.toLocaleString("pt-BR", { maximumFractionDigits: 2 })
}

function Badges({ items }: { items: string[] }) {
  return (
    <div className="flex flex-wrap gap-1.5">
      {items.map((item) => (
        <span
          key={item}
          className="rounded border border-border bg-secondary/50 px-2 py-0.5 text-xs"
        >
          {item}
        </span>
      ))}
    </div>
  )
}

export function AnalyzeResultPanel({ file }: AnalyzeResultPanelProps) {
  const [cleanBefore, setCleanBefore] = useState(true)
  const [normalizeBr, setNormalizeBr] = useState(true)
  const [result, setResult] = useState<AnalyzePreviewResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const run = async () => {
    setLoading(true)
    setError(null)
    const options: AnalyzeOptions = {
      cleanBeforeAnalyze: cleanBefore,
      normalizeBr,
    }
    try {
      setResult(await analyzePreview(file, options))
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "Erro ao analisar a planilha.")
    } finally {
      setLoading(false)
    }
  }

  const normalizedColumns = result
    ? [...result.normalized_numeric_columns, ...result.normalized_date_columns]
    : []

  return (
    <section className="rounded-lg border border-border bg-card p-5">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h3 className="text-sm font-medium">Analisar planilha</h3>
          <p className="mt-0.5 text-xs text-muted-foreground">
            Resumo, qualidade dos dados, colunas e estatísticas.
          </p>
        </div>
        <ActionButton onClick={run} loading={loading} icon={BarChart3}>
          Analisar planilha
        </ActionButton>
      </div>

      <div className="mt-4 flex flex-col gap-3 border-t border-border pt-4">
        <label className="flex items-center gap-2.5 text-sm">
          <input
            type="checkbox"
            checked={cleanBefore}
            onChange={(e) => setCleanBefore(e.target.checked)}
            className="size-4 rounded border-border accent-[#1f1f1f]"
          />
          Limpar antes de analisar
        </label>
        <label className="flex items-center gap-2.5 text-sm">
          <input
            type="checkbox"
            checked={normalizeBr}
            onChange={(e) => setNormalizeBr(e.target.checked)}
            className="size-4 rounded border-border accent-[#1f1f1f]"
          />
          Normalizar dados brasileiros
        </label>
        <p className="text-xs leading-relaxed text-muted-foreground">
          Normalização brasileira reconhece valores como R$ 1.234,56 e datas como
          31/12/2026 antes de calcular as estatísticas.
        </p>
      </div>

      {error && (
        <div className="mt-4">
          <ErrorNote message={error} />
        </div>
      )}

      {result && (
        <div className="mt-5 flex flex-col gap-5">
          {/* Resumo geral */}
          <Section title="Resumo geral">
            <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
              <div>
                <p className="text-xs text-muted-foreground">Linhas</p>
                <p className="mt-0.5 text-lg font-semibold">
                  {num(result.rows_count)}
                </p>
              </div>
              <div>
                <p className="text-xs text-muted-foreground">Colunas</p>
                <p className="mt-0.5 text-lg font-semibold">
                  {num(result.columns_count)}
                </p>
              </div>
              <div>
                <p className="text-xs text-muted-foreground">Valores ausentes</p>
                <p className="mt-0.5 text-lg font-semibold">
                  {num(result.missing_values_count)}
                </p>
              </div>
              <div>
                <p className="text-xs text-muted-foreground">Duplicatas</p>
                <p className="mt-0.5 text-lg font-semibold">
                  {num(result.duplicate_rows_count)}
                </p>
              </div>
            </div>
          </Section>

          {/* Colunas normalizadas */}
          {normalizedColumns.length > 0 && (
            <Section title="Colunas normalizadas (BR)">
              <Badges items={normalizedColumns} />
            </Section>
          )}

          {/* Colunas detectadas */}
          {result.column_summaries.length > 0 && (
            <Section title="Colunas detectadas">
              <div className="overflow-x-auto rounded-lg border border-border">
                <table className="w-full border-collapse text-sm">
                  <thead>
                    <tr className="border-b border-border bg-secondary/50 text-xs text-muted-foreground">
                      <th className="px-3 py-2 text-left font-medium">Coluna</th>
                      <th className="px-3 py-2 text-left font-medium">Tipo</th>
                      <th className="px-3 py-2 text-right font-medium">
                        Ausentes
                      </th>
                      <th className="px-3 py-2 text-right font-medium">
                        Únicos
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {result.column_summaries.map((col) => (
                      <tr
                        key={col.name}
                        className="border-b border-border last:border-0"
                      >
                        <td className="px-3 py-2.5 font-medium">{col.name}</td>
                        <td className="px-3 py-2.5 text-muted-foreground">
                          {col.dtype}
                        </td>
                        <td className="px-3 py-2.5 text-right tabular-nums">
                          {num(col.missing_count)}
                          <span className="ml-1 text-xs text-muted-foreground">
                            ({num(col.missing_percentage)}%)
                          </span>
                        </td>
                        <td className="px-3 py-2.5 text-right tabular-nums">
                          {num(col.unique_count)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </Section>
          )}

          {/* Estatísticas numéricas */}
          {result.numeric_summaries.length > 0 && (
            <Section title="Estatísticas numéricas">
              <div className="overflow-x-auto rounded-lg border border-border">
                <table className="w-full border-collapse text-sm">
                  <thead>
                    <tr className="border-b border-border bg-secondary/50 text-xs text-muted-foreground">
                      <th className="px-3 py-2 text-left font-medium">Coluna</th>
                      <th className="px-3 py-2 text-right font-medium">
                        Contagem
                      </th>
                      <th className="px-3 py-2 text-right font-medium">Média</th>
                      <th className="px-3 py-2 text-right font-medium">Mín</th>
                      <th className="px-3 py-2 text-right font-medium">Máx</th>
                      <th className="px-3 py-2 text-right font-medium">Soma</th>
                    </tr>
                  </thead>
                  <tbody>
                    {result.numeric_summaries.map((stat) => (
                      <tr
                        key={stat.name}
                        className="border-b border-border last:border-0"
                      >
                        <td className="px-3 py-2.5 font-medium">{stat.name}</td>
                        <td className="px-3 py-2.5 text-right tabular-nums">
                          {num(stat.count)}
                        </td>
                        <td className="px-3 py-2.5 text-right tabular-nums">
                          {num(stat.mean)}
                        </td>
                        <td className="px-3 py-2.5 text-right tabular-nums">
                          {num(stat.min)}
                        </td>
                        <td className="px-3 py-2.5 text-right tabular-nums">
                          {num(stat.max)}
                        </td>
                        <td className="px-3 py-2.5 text-right tabular-nums">
                          {num(stat.sum)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </Section>
          )}

          {/* Valores mais frequentes */}
          {result.categorical_summaries.length > 0 && (
            <Section title="Valores mais frequentes">
              <div className="grid gap-4 sm:grid-cols-2">
                {result.categorical_summaries.map((cat) => (
                  <div
                    key={cat.name}
                    className="rounded-lg border border-border p-4"
                  >
                    <div className="mb-3 flex items-baseline justify-between gap-2">
                      <p className="text-sm font-medium">{cat.name}</p>
                      <span className="text-xs text-muted-foreground">
                        {num(cat.unique_count)} únicos
                      </span>
                    </div>
                    <ul className="flex flex-col gap-2">
                      {cat.top_values.map((v) => (
                        <li
                          key={v.value}
                          className="flex items-center justify-between gap-3 text-sm"
                        >
                          <span className="truncate text-muted-foreground">
                            {v.value || "—"}
                          </span>
                          <span className="tabular-nums text-foreground">
                            {num(v.count)}
                          </span>
                        </li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>
            </Section>
          )}

          {/* Datas detectadas */}
          {result.date_summaries.length > 0 && (
            <Section title="Datas detectadas">
              <div className="overflow-x-auto rounded-lg border border-border">
                <table className="w-full border-collapse text-sm">
                  <thead>
                    <tr className="border-b border-border bg-secondary/50 text-xs text-muted-foreground">
                      <th className="px-3 py-2 text-left font-medium">Coluna</th>
                      <th className="px-3 py-2 text-left font-medium">Início</th>
                      <th className="px-3 py-2 text-left font-medium">Fim</th>
                      <th className="px-3 py-2 text-right font-medium">
                        Datas válidas
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {result.date_summaries.map((date) => (
                      <tr
                        key={date.name}
                        className="border-b border-border last:border-0"
                      >
                        <td className="px-3 py-2.5 font-medium">{date.name}</td>
                        <td className="px-3 py-2.5 text-muted-foreground">
                          {date.min_date ?? "—"}
                        </td>
                        <td className="px-3 py-2.5 text-muted-foreground">
                          {date.max_date ?? "—"}
                        </td>
                        <td className="px-3 py-2.5 text-right tabular-nums">
                          {num(date.valid_dates_count)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </Section>
          )}
        </div>
      )}
    </section>
  )
}
