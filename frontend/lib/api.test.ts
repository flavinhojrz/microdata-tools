import { describe, expect, it } from "vitest"
import {
  analyzeExtraFields,
  buildFormData,
  convertExtraFields,
  parseContentDispositionFilename,
} from "@/lib/api"

function makeFile(name = "dados.csv"): File {
  return new File(["a,b\n1,2\n"], name, { type: "text/csv" })
}

describe("buildFormData", () => {
  it("inclui sempre o arquivo no campo 'file'", () => {
    const file = makeFile()
    const form = buildFormData(file)

    const sent = form.get("file")
    expect(sent).toBeInstanceOf(File)
    expect((sent as File).name).toBe("dados.csv")
  })

  it("anexa campos extras como strings", () => {
    const form = buildFormData(makeFile(), { target_format: "json", x: "1" })

    expect(form.get("target_format")).toBe("json")
    expect(form.get("x")).toBe("1")
  })

  it("não adiciona campos extras quando não há nenhum", () => {
    const form = buildFormData(makeFile())
    const keys = [...form.keys()]

    expect(keys).toEqual(["file"])
  })
})

describe("convertExtraFields", () => {
  it("serializa formato, flags e nome da tabela", () => {
    const fields = convertExtraFields({
      format: "sql",
      cleanBeforeConvert: true,
      normalizeBr: false,
      tableName: "vendas",
    })

    expect(fields).toEqual({
      target_format: "sql",
      clean_before_convert: "true",
      normalize_brazilian_data: "false",
      table_name: "vendas",
    })
  })

  it("omite table_name quando ausente", () => {
    const fields = convertExtraFields({
      format: "json",
      cleanBeforeConvert: false,
      normalizeBr: true,
    })

    expect(fields).toEqual({
      target_format: "json",
      clean_before_convert: "false",
      normalize_brazilian_data: "true",
    })
    expect(fields).not.toHaveProperty("table_name")
  })
})

describe("analyzeExtraFields", () => {
  it("serializa as flags booleanas como string", () => {
    expect(
      analyzeExtraFields({ cleanBeforeAnalyze: true, normalizeBr: false }),
    ).toEqual({
      clean_before_analyze: "true",
      normalize_brazilian_data: "false",
    })
  })
})

describe("parseContentDispositionFilename", () => {
  it("retorna null quando não há header", () => {
    expect(parseContentDispositionFilename(null)).toBeNull()
  })

  it("extrai filename simples entre aspas", () => {
    expect(
      parseContentDispositionFilename('attachment; filename="dados.json"'),
    ).toBe("dados.json")
  })

  it("extrai filename sem aspas", () => {
    expect(
      parseContentDispositionFilename("attachment; filename=dados.csv"),
    ).toBe("dados.csv")
  })

  it("prefere e decodifica a variante UTF-8", () => {
    expect(
      parseContentDispositionFilename(
        "attachment; filename=\"fallback.csv\"; filename*=UTF-8''rela%C3%A7%C3%A3o.csv",
      ),
    ).toBe("relação.csv")
  })
})
