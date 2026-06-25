import type { FilePreviewResult } from "@/types"
import { DataPreviewTable } from "@/components/data-preview-table"

interface FilePreviewProps {
  preview: FilePreviewResult
}

function Meta({ label, value }: { label: string; value: string | number }) {
  return (
    <div>
      <dt className="text-xs text-muted-foreground">{label}</dt>
      <dd className="mt-0.5 text-sm font-medium text-foreground">{value}</dd>
    </div>
  )
}

export function FilePreview({ preview }: FilePreviewProps) {
  return (
    <section className="rounded-lg border border-border bg-card p-5">
      <div className="flex items-center justify-between gap-3">
        <h3 className="text-sm font-medium">Prévia do arquivo</h3>
        <span className="text-xs text-muted-foreground">
          Detectamos as colunas automaticamente.
        </span>
      </div>

      <dl className="mt-4 grid grid-cols-2 gap-4 border-t border-border pt-4 sm:grid-cols-4">
        <Meta label="Arquivo" value={preview.filename} />
        <Meta label="Extensão" value={preview.extension || "—"} />
        <Meta
          label="Delimitador"
          value={preview.delimiter ? `"${preview.delimiter}"` : "—"}
        />
        <Meta label="Linhas" value={preview.rows_count.toLocaleString("pt-BR")} />
        <Meta label="Colunas" value={preview.columns_count} />
      </dl>

      {preview.columns?.length > 0 && (
        <div className="mt-4 border-t border-border pt-4">
          <p className="mb-2 text-xs text-muted-foreground">
            Colunas detectadas
          </p>
          <div className="flex flex-wrap gap-1.5">
            {preview.columns.map((col) => (
              <span
                key={col}
                className="rounded border border-border bg-secondary/50 px-2 py-0.5 text-xs text-foreground"
              >
                {col}
              </span>
            ))}
          </div>
        </div>
      )}

      {preview.preview?.length > 0 && (
        <div className="mt-4 border-t border-border pt-4">
          <p className="mb-2 text-xs text-muted-foreground">Primeiras linhas</p>
          <DataPreviewTable columns={preview.columns} rows={preview.preview} />
        </div>
      )}
    </section>
  )
}
