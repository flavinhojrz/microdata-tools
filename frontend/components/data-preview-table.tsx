interface DataPreviewTableProps {
  columns: string[]
  rows: Record<string, unknown>[]
}

function formatCell(value: unknown): string {
  if (value === null || value === undefined || value === "") return "—"
  if (typeof value === "object") return JSON.stringify(value)
  return String(value)
}

export function DataPreviewTable({ columns, rows }: DataPreviewTableProps) {
  if (!columns.length) return null

  return (
    <div className="overflow-x-auto rounded-lg border border-border">
      <table className="w-full border-collapse text-sm">
        <thead>
          <tr className="border-b border-border bg-secondary/50">
            {columns.map((col) => (
              <th
                key={col}
                className="whitespace-nowrap px-3 py-2 text-left text-xs font-medium text-muted-foreground"
              >
                {col}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, i) => (
            <tr
              key={i}
              className="border-b border-border last:border-0 hover:bg-secondary/30"
            >
              {columns.map((col) => {
                const text = formatCell(row[col])
                return (
                  <td
                    key={col}
                    className={`whitespace-nowrap px-3 py-2.5 ${
                      text === "—"
                        ? "text-muted-foreground/60"
                        : "text-foreground"
                    }`}
                  >
                    {text}
                  </td>
                )
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
