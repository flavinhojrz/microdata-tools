"use client"

import { useState } from "react"
import { Download, Eraser } from "lucide-react"
import type { CleanPreviewResult } from "@/types"
import {
  ApiError,
  cleanDownload,
  cleanPreview,
  downloadBlob,
} from "@/lib/api"
import { ActionButton, ErrorNote, SuccessNote } from "@/components/panel-ui"

interface CleanResultPanelProps {
  file: File
}

function StatBlock({
  label,
  value,
  hint,
}: {
  label: string
  value: number | string
  hint?: string
}) {
  return (
    <div className="rounded-md border border-border bg-card p-4">
      <p className="text-xs text-muted-foreground">{label}</p>
      <p className="mt-1 text-xl font-semibold tracking-tight">{value}</p>
      {hint && <p className="mt-0.5 text-xs text-muted-foreground">{hint}</p>}
    </div>
  )
}

export function CleanResultPanel({ file }: CleanResultPanelProps) {
  const [result, setResult] = useState<CleanPreviewResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [downloading, setDownloading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const run = async () => {
    setLoading(true)
    setError(null)
    try {
      setResult(await cleanPreview(file))
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "Erro ao limpar o arquivo.")
    } finally {
      setLoading(false)
    }
  }

  const download = async () => {
    setDownloading(true)
    setError(null)
    try {
      const { blob, filename } = await cleanDownload(file)
      const base = file.name.replace(/\.[^.]+$/, "")
      downloadBlob(blob, filename ?? `${base}-limpo.csv`)
    } catch (e) {
      setError(
        e instanceof ApiError ? e.message : "Erro ao baixar o arquivo limpo.",
      )
    } finally {
      setDownloading(false)
    }
  }

  return (
    <section className="rounded-lg border border-border bg-card p-5">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h3 className="text-sm font-medium">Limpar arquivo</h3>
          <p className="mt-0.5 text-xs text-muted-foreground">
            Remove linhas e colunas vazias, duplicatas e padroniza colunas.
          </p>
        </div>
        <ActionButton onClick={run} loading={loading} icon={Eraser}>
          Gerar prévia
        </ActionButton>
      </div>

      {error && (
        <div className="mt-4">
          <ErrorNote message={error} />
        </div>
      )}

      {result && (
        <div className="mt-5 border-t border-border pt-5">
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
            <StatBlock
              label="Linhas"
              value={`${result.original_rows_count} → ${result.cleaned_rows_count}`}
            />
            <StatBlock
              label="Colunas"
              value={`${result.original_columns_count} → ${result.cleaned_columns_count}`}
            />
            <StatBlock
              label="Linhas vazias removidas"
              value={result.removed_empty_rows_count}
            />
            <StatBlock
              label="Colunas vazias removidas"
              value={result.removed_empty_columns_count}
            />
            <StatBlock
              label="Duplicatas removidas"
              value={result.removed_duplicate_rows_count}
            />
          </div>

          <div className="mt-5 flex flex-wrap items-center gap-3">
            <ActionButton
              onClick={download}
              loading={downloading}
              icon={Download}
              variant="secondary"
            >
              Baixar CSV limpo
            </ActionButton>
            {!downloading && <SuccessNote message="Prévia gerada" />}
          </div>
        </div>
      )}
    </section>
  )
}
