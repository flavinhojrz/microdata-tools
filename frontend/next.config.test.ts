import { afterEach, describe, expect, it, vi } from "vitest"

// O guard de produção vive no topo de next.config.ts e roda na avaliação do
// módulo. Importamos o config dinamicamente, com o ambiente manipulado, para
// garantir que o build de produção falha quando a API não está configurada
// corretamente — sem precisar rodar um `next build` real no CI.
afterEach(() => {
  vi.unstubAllEnvs()
  vi.resetModules()
})

function loadConfig() {
  return import("@/next.config")
}

describe("next.config guard de produção", () => {
  it("falha o build de produção sem NEXT_PUBLIC_API_BASE_URL", async () => {
    vi.stubEnv("NODE_ENV", "production")
    vi.stubEnv("NEXT_PUBLIC_API_BASE_URL", "")

    await expect(loadConfig()).rejects.toThrow(/obrigatória em produção/)
  })

  it("falha o build de produção com URL HTTP (exige HTTPS)", async () => {
    vi.stubEnv("NODE_ENV", "production")
    vi.stubEnv("NEXT_PUBLIC_API_BASE_URL", "http://api.exemplo.com")

    await expect(loadConfig()).rejects.toThrow(/HTTPS em produção/)
  })

  it("aceita URL HTTPS em produção", async () => {
    vi.stubEnv("NODE_ENV", "production")
    vi.stubEnv("NEXT_PUBLIC_API_BASE_URL", "https://api.exemplo.com")

    const mod = await loadConfig()

    expect(mod.default).toBeDefined()
  })

  it("aceita URL HTTP apenas em desenvolvimento", async () => {
    vi.stubEnv("NODE_ENV", "development")
    vi.stubEnv("NEXT_PUBLIC_API_BASE_URL", "http://127.0.0.1:8000")

    const mod = await loadConfig()

    expect(mod.default).toBeDefined()
  })
})
