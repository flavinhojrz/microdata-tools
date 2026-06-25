"use client"

import { useRef, useState } from "react"
import { FileSpreadsheet, Loader2 } from "lucide-react"
import type { FilePreviewResult, ToolId } from "@/types"
import { ApiError, previewFile } from "@/lib/api"
import { AppHeader } from "@/components/app-header"
import { HeroSection } from "@/components/hero-section"
import { UploadDropzone } from "@/components/upload-dropzone"
import { ToolSelector } from "@/components/tool-selector"
import { FilePreview } from "@/components/file-preview"
import { CleanResultPanel } from "@/components/clean-result-panel"
import { ConvertResultPanel } from "@/components/convert-result-panel"
import { AnalyzeResultPanel } from "@/components/analyze-result-panel"
import { EmptyState } from "@/components/empty-state"
import { ErrorNote } from "@/components/panel-ui"
import { Footer } from "@/components/footer"

export default function Page() {
  const [file, setFile] = useState<File | null>(null)
  const [preview, setPreview] = useState<FilePreviewResult | null>(null)
  const [previewLoading, setPreviewLoading] = useState(false)
  const [previewError, setPreviewError] = useState<string | null>(null)
  const [tool, setTool] = useState<ToolId>("clean")

  const toolsRef = useRef<HTMLDivElement>(null)

  const scrollToTools = () => {
    toolsRef.current?.scrollIntoView({ behavior: "smooth", block: "start" })
  }

  const handleFileSelect = async (selected: File) => {
    setFile(selected)
    setPreview(null)
    setPreviewError(null)
    setPreviewLoading(true)
    try {
      setPreview(await previewFile(selected))
    } catch (e) {
      setPreviewError(
        e instanceof ApiError ? e.message : "Erro ao ler a prévia do arquivo.",
      )
    } finally {
      setPreviewLoading(false)
    }
  }

  const handleClear = () => {
    setFile(null)
    setPreview(null)
    setPreviewError(null)
  }

  return (
    <div className="min-h-screen bg-background text-foreground">
      <AppHeader />

      <main>
        <HeroSection onUploadClick={scrollToTools} onToolsClick={scrollToTools} />

        <div
          id="ferramentas"
          ref={toolsRef}
          className="mx-auto max-w-6xl scroll-mt-20 px-5 pb-4"
        >
          <div className="grid gap-5 lg:grid-cols-2">
            {/* Coluna esquerda: upload */}
            <div>
              <h2 className="mb-3 text-sm font-medium">Enviar planilha</h2>
              <UploadDropzone
                file={file}
                onFileSelect={handleFileSelect}
                onClear={handleClear}
              />
            </div>

            {/* Coluna direita: seleção de ferramenta */}
            <ToolSelector selected={tool} onSelect={setTool} />
          </div>
        </div>

        <div className="mx-auto max-w-6xl px-5 pb-12">
          {!file && (
            <div className="mt-6">
              <EmptyState
                icon={FileSpreadsheet}
                title="Envie um arquivo para começar."
                description="Ideal para planilhas de vendas, maquininhas, relatórios e dados bagunçados."
              />
            </div>
          )}

          {previewLoading && (
            <div className="mt-6 flex items-center justify-center gap-2 rounded-lg border border-border bg-card py-12 text-sm text-muted-foreground">
              <Loader2 className="size-4 animate-spin" strokeWidth={1.5} />
              Lendo o arquivo...
            </div>
          )}

          {previewError && (
            <div className="mt-6">
              <ErrorNote message={previewError} />
            </div>
          )}

          {preview && (
            <div className="mt-6 flex flex-col gap-6">
              <FilePreview preview={preview} />
              {tool === "clean" && <CleanResultPanel file={file!} />}
              {tool === "convert" && <ConvertResultPanel file={file!} />}
              {tool === "analyze" && <AnalyzeResultPanel file={file!} />}
            </div>
          )}
        </div>
      </main>

      <Footer />
    </div>
  )
}
