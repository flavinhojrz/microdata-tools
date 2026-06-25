"use client"

import { useRef, useState } from "react"
import { FileSpreadsheet, Upload, X } from "lucide-react"

const ACCEPTED = [".csv", ".xlsx", ".xls"]
const MAX_BYTES = 10 * 1024 * 1024 // 10 MB

interface UploadDropzoneProps {
  file: File | null
  onFileSelect: (file: File) => void
  onClear: () => void
}

function formatSize(bytes: number) {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(0)} KB`
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

export function UploadDropzone({
  file,
  onFileSelect,
  onClear,
}: UploadDropzoneProps) {
  const inputRef = useRef<HTMLInputElement>(null)
  const [dragging, setDragging] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const validateAndSelect = (selected: File | undefined) => {
    setError(null)
    if (!selected) return
    const name = selected.name.toLowerCase()
    const okExt = ACCEPTED.some((ext) => name.endsWith(ext))
    if (!okExt) {
      setError("Formato não suportado. Use .csv, .xlsx ou .xls.")
      return
    }
    if (selected.size > MAX_BYTES) {
      setError("Arquivo acima de 10 MB.")
      return
    }
    onFileSelect(selected)
  }

  if (file) {
    return (
      <div className="rounded-lg border border-border bg-card p-5">
        <div className="flex items-start justify-between gap-3">
          <div className="flex items-center gap-3">
            <div className="flex size-9 items-center justify-center rounded-md bg-secondary">
              <FileSpreadsheet
                className="size-4 text-foreground"
                strokeWidth={1.5}
              />
            </div>
            <div className="min-w-0">
              <p className="truncate text-sm font-medium">{file.name}</p>
              <p className="text-xs text-muted-foreground">
                {formatSize(file.size)}
              </p>
            </div>
          </div>
          <button
            type="button"
            onClick={onClear}
            className="inline-flex items-center gap-1 rounded-md px-2 py-1 text-xs text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground"
          >
            <X className="size-3.5" strokeWidth={1.5} />
            Remover
          </button>
        </div>
      </div>
    )
  }

  return (
    <div>
      <input
        ref={inputRef}
        type="file"
        accept={ACCEPTED.join(",")}
        className="sr-only"
        onChange={(e) => validateAndSelect(e.target.files?.[0])}
      />
      <button
        type="button"
        onClick={() => inputRef.current?.click()}
        onDragOver={(e) => {
          e.preventDefault()
          setDragging(true)
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={(e) => {
          e.preventDefault()
          setDragging(false)
          validateAndSelect(e.dataTransfer.files?.[0])
        }}
        className={`flex w-full flex-col items-center justify-center rounded-lg border border-dashed px-6 py-12 text-center transition-colors ${
          dragging
            ? "border-foreground/40 bg-secondary"
            : "border-border bg-card hover:bg-secondary/40"
        }`}
      >
        <div className="mb-4 flex size-10 items-center justify-center rounded-full border border-border bg-background">
          <Upload className="size-4 text-muted-foreground" strokeWidth={1.5} />
        </div>
        <p className="text-sm font-medium">
          Arraste um arquivo aqui ou clique para selecionar
        </p>
        <p className="mt-1 text-xs text-muted-foreground">
          Formatos aceitos: .csv, .xlsx, .xls · até 10 MB
        </p>
        <span className="mt-5 inline-flex items-center rounded-md border border-border bg-background px-3 py-1.5 text-sm font-medium text-foreground">
          Selecionar arquivo
        </span>
      </button>

      {error ? (
        <p className="mt-3 text-xs text-destructive">{error}</p>
      ) : (
        <p className="mt-3 text-xs text-muted-foreground">
          Arquivos processados apenas para gerar o resultado.
        </p>
      )}
    </div>
  )
}
