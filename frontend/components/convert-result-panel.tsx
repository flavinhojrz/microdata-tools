"use client"

import { useState } from "react"
import { Download, Replace } from "lucide-react"
import type { ConvertFormat, ConvertPreviewResult } from "@/types"
import {
  ApiError,
  convertDownload,
  convertPreview,
  downloadBlob,
  type ConvertOptions,
} from "@/lib/api"
import { ActionButton, ErrorNote, SuccessNote } from "@/components/panel-ui"

interface ConvertResultPanelProps {
  file: File
}

const formats: { id: ConvertFormat; label: string; ext: string }[] = [
  { id: "json", label: "JSON", ext: "json" },
  { id: "markdown", label: "Markdown", ext: "md" },
  { id: "sql", label: "SQL", ext: "sql" },
]

export function ConvertResultPanel({ file }: ConvertResultPanelProps) {
  const [format, setFormat] = useState<ConvertFormat>("json")
  const [cleanBefore, setCleanBefore] = useState(true)
  const [normalizeBr, setNormalizeBr] = useState(true)
  const [tableName, setTableName] = useState("dados")
  const [result, setResult] = useState<ConvertPreviewResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [downloading, setDownloading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const buildOptions = (): ConvertOptions => ({
    format,
    cleanBeforeConvert: cleanBefore,
    normalizeBr,
    tableName: format === "sql" ? tableName : undefined,
  })

  const run = async () => {
    setLoading(true)
    setError(null)
    try {
      setResult(await convertPreview(file, buildOptions()))
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "Erro ao converter o arquivo.")
    } finally {
      setLoading(false)
    }
  }

  const download = async () => {
    setDownloading(true)
    setError(null)
    try {
      const { blob, filename } = await convertDownload(file, buildOptions())
      const base = file.name.replace(/\.[^.]+$/, "")
      const ext = formats.find((f) => f.id === format)?.ext ?? "txt"
      downloadBlob(blob, filename ?? `${base}.${ext}`)
    } catch (e) {
      setError(
        e instanceof ApiError ? e.message : "Erro ao baixar o arquivo convertido.",
      )
    } finally {
      setDownloading(false)
    }
  }

  return (
    <section className="rounded-lg border border-border bg-card p-5">
      <div>
        <h3 className="text-sm font-medium">Converter arquivo</h3>
        <p className="mt-0.5 text-xs text-muted-foreground">
          Você pode limpar antes de converter.
        </p>
      </div>

      <div className="mt-4 border-t border-border pt-4">
        <p className="mb-2 text-xs text-muted-foreground">Formato de saída</p>
        <div className="inline-flex rounded-md border border-border p-0.5">
          {formats.map((f) => (
            <button
              key={f.id}
              type="button"
              onClick={() => setFormat(f.id)}
              className={`rounded px-3 py-1.5 text-sm transition-colors ${
                format === f.id
                  ? "bg-primary text-primary-foreground"
                  : "text-muted-foreground hover:text-foreground"
              }`}
            >
              {f.label}
            </button>
          ))}
        </div>
      </div>

      <div className="mt-4 flex flex-col gap-3 border-t border-border pt-4">
        <label className="flex items-center gap-2.5 text-sm">
          <input
            type="checkbox"
            checked={cleanBefore}
            onChange={(e) => setCleanBefore(e.target.checked)}
            className="size-4 rounded border-border accent-[#1f1f1f]"
          />
          Limpar antes de converter
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
          31/12/2026.
        </p>

        {format === "sql" && (
          <div className="mt-1">
            <label
              htmlFor="table-name"
              className="mb-1.5 block text-xs text-muted-foreground"
            >
              Nome da tabela SQL
            </label>
            <input
              id="table-name"
              type="text"
              value={tableName}
              onChange={(e) => setTableName(e.target.value)}
              className="w-full max-w-xs rounded-md border border-border bg-background px-3 py-1.5 text-sm outline-none focus:border-foreground/30"
            />
          </div>
        )}
      </div>

      <div className="mt-4 flex flex-wrap items-center gap-3 border-t border-border pt-4">
        <ActionButton onClick={run} loading={loading} icon={Replace}>
          Gerar prévia
        </ActionButton>
        {result && (
          <ActionButton
            onClick={download}
            loading={downloading}
            icon={Download}
            variant="secondary"
          >
            Baixar arquivo convertido
          </ActionButton>
        )}
        {result && !downloading && <SuccessNote message="Prévia gerada" />}
      </div>

      {error && (
        <div className="mt-4">
          <ErrorNote message={error} />
        </div>
      )}

      {result && (
        <div className="mt-5 border-t border-border pt-5">
          <p className="mb-2 text-xs text-muted-foreground">Prévia</p>
          <pre className="max-h-96 overflow-auto rounded-lg border border-border bg-code p-4 font-mono text-xs leading-relaxed text-foreground">
            {result.content_preview}
          </pre>
        </div>
      )}
    </section>
  )
}
