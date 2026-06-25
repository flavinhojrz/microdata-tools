import type { NextConfig } from "next"

const isDev = process.env.NODE_ENV === "development"

const rawApiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL

// Em produção a URL da API é obrigatória e precisa ser HTTPS: os arquivos do
// usuário são enviados diretamente para ela. Falhar o build cedo evita publicar
// um bundle que vaza uploads para o host errado ou trafega em HTTP.
if (process.env.NODE_ENV === "production") {
  if (!rawApiBaseUrl) {
    throw new Error("NEXT_PUBLIC_API_BASE_URL é obrigatória em produção.")
  }

  if (!rawApiBaseUrl.startsWith("https://")) {
    throw new Error("NEXT_PUBLIC_API_BASE_URL deve usar HTTPS em produção.")
  }
}

// Mesma base usada pelo cliente (lib/api.ts): precisa ser permitida em connect-src.
// O fallback HTTP só é alcançável em dev (em produção o guard acima já barrou).
const apiBaseUrl = (rawApiBaseUrl ?? "http://127.0.0.1:8000").replace(/\/+$/, "")

// CSP inicial sem nonce (header-only). Mais permissiva que uma política com
// nonce/proxy, mas não quebra a hidratação inline do Next nem o build estático.
// Para endurecer, migrar para nonce via proxy.ts (ver guia de CSP do Next).
const cspHeader = [
  "default-src 'self'",
  `script-src 'self' 'unsafe-inline'${isDev ? " 'unsafe-eval'" : ""}`,
  "style-src 'self' 'unsafe-inline'",
  // O botão oficial do Buy Me a Coffee é servido como imagem por este host.
  "img-src 'self' blob: data: https://img.buymeacoffee.com",
  "font-src 'self' data:",
  `connect-src 'self' ${apiBaseUrl}${isDev ? " ws:" : ""}`,
  "object-src 'none'",
  "base-uri 'self'",
  "form-action 'self'",
  "frame-ancestors 'none'",
  // Só em produção (HTTPS). Em dev o server é HTTP: isto faria o navegador
  // tentar buscar CSS/JS via https://localhost e quebraria todo o CSS.
  ...(isDev ? [] : ["upgrade-insecure-requests"]),
].join("; ")

const securityHeaders = [
  { key: "Content-Security-Policy", value: cspHeader },
  { key: "X-Content-Type-Options", value: "nosniff" },
  { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
  { key: "X-Frame-Options", value: "DENY" },
  {
    key: "Permissions-Policy",
    value: "camera=(), microphone=(), geolocation=(), interest-cohort=()",
  },
]

const nextConfig: NextConfig = {
  poweredByHeader: false,
  async headers() {
    return [{ source: "/:path*", headers: securityHeaders }]
  },
}

export default nextConfig
