import type {
  AnalyzePreviewResult,
  CleanPreviewResult,
  ConvertFormat,
  ConvertPreviewResult,
  FilePreviewResult,
} from "@/types"

/**
 * Base da API. Configure via NEXT_PUBLIC_API_BASE_URL (ver .env.example).
 * ATENÇÃO: os arquivos enviados pelo usuário vão diretamente para esta URL.
 * Em produção, aponte sempre para um host de confiança (HTTPS).
 */
const rawApiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL

// O fallback HTTP serve apenas para desenvolvimento local. Em produção o build
// (ver next.config.ts) exige NEXT_PUBLIC_API_BASE_URL HTTPS, então este default
// nunca é usado num bundle publicado.
export const API_BASE_URL = (rawApiBaseUrl ?? "http://127.0.0.1:8000").replace(
  /\/+$/,
  "",
)

/** Timeout padrão das requisições de preview/JSON (ms). */
const DEFAULT_TIMEOUT_MS = 30_000
/** Downloads podem processar arquivos maiores; damos mais folga. */
const DOWNLOAD_TIMEOUT_MS = 60_000

/** Erro de API com mensagem amigável já tratada para exibição. */
export class ApiError extends Error {
  status?: number
  constructor(message: string, status?: number) {
    super(message)
    this.name = "ApiError"
    this.status = status
  }
}

async function parseError(res: Response): Promise<never> {
  let message = `Não foi possível processar o arquivo (erro ${res.status}).`
  try {
    const data = await res.json()
    if (typeof data?.detail === "string") message = data.detail
    else if (Array.isArray(data?.detail) && data.detail[0]?.msg)
      message = data.detail[0].msg
    else if (typeof data?.message === "string") message = data.message
  } catch {
    // resposta não-JSON, mantém a mensagem padrão
  }
  throw new ApiError(message, res.status)
}

export function buildFormData(
  file: File,
  extra?: Record<string, string>,
): FormData {
  const formData = new FormData()
  formData.append("file", file)
  if (extra) {
    for (const [key, value] of Object.entries(extra)) {
      formData.append(key, value)
    }
  }
  return formData
}

/**
 * Faz o POST do arquivo com timeout/cancelamento via AbortController e sem
 * enviar credenciais (a API não usa cookies/sessão).
 */
async function postFile(
  path: string,
  file: File,
  extra: Record<string, string> | undefined,
  timeoutMs: number,
): Promise<Response> {
  const controller = new AbortController()
  const timeout = setTimeout(() => controller.abort(), timeoutMs)

  let res: Response
  try {
    res = await fetch(`${API_BASE_URL}${path}`, {
      method: "POST",
      body: buildFormData(file, extra),
      credentials: "omit",
      signal: controller.signal,
    })
  } catch (error) {
    if (error instanceof DOMException && error.name === "AbortError") {
      throw new ApiError(
        "A requisição demorou demais e foi cancelada. Tente novamente.",
      )
    }
    throw new ApiError(
      "Não foi possível conectar ao servidor. Verifique se a API está disponível.",
    )
  } finally {
    clearTimeout(timeout)
  }

  if (!res.ok) return parseError(res)
  return res
}

async function postJson<T>(
  path: string,
  file: File,
  extra?: Record<string, string>,
): Promise<T> {
  const res = await postFile(path, file, extra, DEFAULT_TIMEOUT_MS)
  return (await res.json()) as T
}

export interface DownloadResult {
  blob: Blob
  /** Nome sugerido pelo backend (Content-Disposition), se disponível. */
  filename: string | null
}

async function postDownload(
  path: string,
  file: File,
  extra?: Record<string, string>,
): Promise<DownloadResult> {
  const res = await postFile(path, file, extra, DOWNLOAD_TIMEOUT_MS)
  return {
    blob: await res.blob(),
    filename: parseContentDispositionFilename(
      res.headers.get("content-disposition"),
    ),
  }
}

/** Extrai o filename de um header Content-Disposition, se houver. */
export function parseContentDispositionFilename(
  header: string | null,
): string | null {
  if (!header) return null
  const utf8Match = header.match(/filename\*=UTF-8''([^;]+)/i)
  if (utf8Match) {
    try {
      return decodeURIComponent(utf8Match[1])
    } catch {
      // valor malformado, tenta o filename simples abaixo
    }
  }
  const match = header.match(/filename="?([^";]+)"?/i)
  return match ? match[1] : null
}

export async function checkHealth(): Promise<boolean> {
  const controller = new AbortController()
  const timeout = setTimeout(() => controller.abort(), 5_000)
  try {
    const res = await fetch(`${API_BASE_URL}/health`, {
      method: "GET",
      credentials: "omit",
      signal: controller.signal,
    })
    return res.ok
  } catch {
    return false
  } finally {
    clearTimeout(timeout)
  }
}

export function previewFile(file: File) {
  return postJson<FilePreviewResult>("/api/files/preview", file)
}

export function cleanPreview(file: File) {
  return postJson<CleanPreviewResult>("/api/files/clean-preview", file)
}

export function cleanDownload(file: File) {
  return postDownload("/api/files/clean-download", file)
}

export interface ConvertOptions {
  format: ConvertFormat
  cleanBeforeConvert: boolean
  normalizeBr: boolean
  tableName?: string
}

export function convertExtraFields(
  options: ConvertOptions,
): Record<string, string> {
  return {
    target_format: options.format,
    clean_before_convert: String(options.cleanBeforeConvert),
    normalize_brazilian_data: String(options.normalizeBr),
    ...(options.tableName ? { table_name: options.tableName } : {}),
  }
}

export function convertPreview(file: File, options: ConvertOptions) {
  return postJson<ConvertPreviewResult>(
    "/api/files/convert-preview",
    file,
    convertExtraFields(options),
  )
}

export function convertDownload(file: File, options: ConvertOptions) {
  return postDownload(
    "/api/files/convert-download",
    file,
    convertExtraFields(options),
  )
}

export interface AnalyzeOptions {
  cleanBeforeAnalyze: boolean
  normalizeBr: boolean
}

export function analyzeExtraFields(
  options: AnalyzeOptions,
): Record<string, string> {
  return {
    clean_before_analyze: String(options.cleanBeforeAnalyze),
    normalize_brazilian_data: String(options.normalizeBr),
  }
}

export function analyzePreview(file: File, options: AnalyzeOptions) {
  return postJson<AnalyzePreviewResult>(
    "/api/files/analyze-preview",
    file,
    analyzeExtraFields(options),
  )
}

/** Dispara o download de um Blob no navegador. */
export function downloadBlob(blob: Blob, filename: string) {
  const url = URL.createObjectURL(blob)
  const a = document.createElement("a")
  a.href = url
  a.download = filename
  document.body.appendChild(a)
  a.click()
  a.remove()
  URL.revokeObjectURL(url)
}
