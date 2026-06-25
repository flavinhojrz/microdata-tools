// Tipos compartilhados da aplicação MicroData Tools.
// Espelham os response models do backend FastAPI (app/schemas/*.py).
// Mantenha-os em sincronia com os schemas: campos divergentes quebram a UI.

export type ToolId = "clean" | "convert" | "analyze"

export type ConvertFormat = "json" | "markdown" | "sql"

/** Linha de dados: objeto coluna -> valor. */
export type DataRow = Record<string, unknown>

/** Prévia básica do arquivo enviado: POST /api/files/preview */
export interface FilePreviewResult {
  filename: string
  extension: string
  delimiter: string | null
  rows_count: number
  columns_count: number
  columns: string[]
  /** Primeiras linhas (até 10) como objetos coluna -> valor. */
  preview: DataRow[]
}

/** Resultado da limpeza: POST /api/files/clean-preview */
export interface CleanPreviewResult {
  filename: string
  extension: string
  delimiter: string | null
  original_rows_count: number
  original_columns_count: number
  cleaned_rows_count: number
  cleaned_columns_count: number
  removed_empty_rows_count: number
  removed_empty_columns_count: number
  removed_duplicate_rows_count: number
  original_columns: string[]
  cleaned_columns: string[]
  preview: DataRow[]
}

/** Resultado da conversão: POST /api/files/convert-preview */
export interface ConvertPreviewResult {
  filename: string
  extension: string
  delimiter: string | null
  target_format: ConvertFormat
  clean_before_convert: boolean
  normalize_brazilian_data: boolean
  normalized_numeric_columns: string[]
  normalized_date_columns: string[]
  rows_count: number
  columns_count: number
  columns: string[]
  /** Conteúdo textual já formatado para preview. */
  content_preview: string
}

export interface ColumnSummary {
  name: string
  dtype: string
  missing_count: number
  missing_percentage: number
  unique_count: number
}

export interface NumericSummary {
  name: string
  count: number
  mean: number | null
  min: number | null
  max: number | null
  sum: number | null
}

export interface TopValue {
  value: string
  count: number
}

export interface CategoricalSummary {
  name: string
  unique_count: number
  top_values: TopValue[]
}

export interface DateSummary {
  name: string
  min_date: string | null
  max_date: string | null
  valid_dates_count: number
}

/** Resultado da análise: POST /api/files/analyze-preview */
export interface AnalyzePreviewResult {
  filename: string
  extension: string
  delimiter: string | null
  clean_before_analyze: boolean
  normalize_brazilian_data: boolean
  normalized_numeric_columns: string[]
  normalized_date_columns: string[]
  rows_count: number
  columns_count: number
  columns: string[]
  missing_values_count: number
  duplicate_rows_count: number
  empty_columns_count: number
  column_summaries: ColumnSummary[]
  numeric_summaries: NumericSummary[]
  categorical_summaries: CategoricalSummary[]
  date_summaries: DateSummary[]
}
