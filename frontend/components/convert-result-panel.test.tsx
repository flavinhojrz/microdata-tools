import { describe, expect, it, vi } from "vitest"
import { fireEvent, render, screen } from "@testing-library/react"

// O painel importa o cliente HTTP real; mockamos para um render sem rede.
vi.mock("@/lib/api", () => ({
  ApiError: class ApiError extends Error {},
  convertPreview: vi.fn(),
  convertDownload: vi.fn(),
  downloadBlob: vi.fn(),
}))

import { ConvertResultPanel } from "@/components/convert-result-panel"

function makeFile(): File {
  return new File(["a,b\n1,2\n"], "dados.csv", { type: "text/csv" })
}

describe("ConvertResultPanel", () => {
  it("renderiza título, formatos e ação de prévia", () => {
    render(<ConvertResultPanel file={makeFile()} />)

    expect(
      screen.getByRole("heading", { name: "Converter arquivo" }),
    ).toBeInTheDocument()
    expect(screen.getByRole("button", { name: "JSON" })).toBeInTheDocument()
    expect(screen.getByRole("button", { name: "Markdown" })).toBeInTheDocument()
    expect(screen.getByRole("button", { name: "SQL" })).toBeInTheDocument()
    expect(
      screen.getByRole("button", { name: /Gerar prévia/ }),
    ).toBeInTheDocument()
  })

  it("mostra o campo de nome da tabela só ao escolher SQL", () => {
    render(<ConvertResultPanel file={makeFile()} />)

    // JSON é o formato inicial: sem campo de tabela.
    expect(screen.queryByLabelText("Nome da tabela SQL")).not.toBeInTheDocument()

    fireEvent.click(screen.getByRole("button", { name: "SQL" }))

    expect(screen.getByLabelText("Nome da tabela SQL")).toBeInTheDocument()
  })
})
