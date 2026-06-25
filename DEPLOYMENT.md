# Deployment — MicroData Tools

Guia técnico de publicação do **beta público**. Documentação de produto, design e
motivação fica em [`frontend/README.md`](frontend/README.md); este arquivo cobre
apenas como colocar o sistema no ar com segurança.

## Arquitetura

```
Navegador
   │  HTTPS
   ▼
Frontend (Next.js)  ──►  Vercel
   │  HTTPS (upload direto dos arquivos)
   ▼
Backend (FastAPI)   ──►  Render
```

- **Frontend** publicado no **Vercel** (config em `frontend/vercel.json`).
- **Backend** publicado no **Render** (config em `render.yaml`, na raiz do repo).
- Os arquivos do usuário são enviados **direto do navegador para o backend**. Por
  isso o frontend exige que `NEXT_PUBLIC_API_BASE_URL` seja HTTPS em produção.
- Não há banco de dados nem armazenamento de arquivos: tudo é processado em
  memória e devolvido na resposta.

Domínios assumidos no primeiro deploy:

- Frontend: `https://microdata-tools.vercel.app`
- Backend: `https://microdata-tools-api.onrender.com`

Ao trocar os domínios, atualize `BACKEND_CORS_ORIGINS` (backend) e
`NEXT_PUBLIC_API_BASE_URL` (frontend) de forma consistente.

## Variáveis de ambiente

### Backend (Render)

| Variável | Valor de produção | Observação |
| --- | --- | --- |
| `ENVIRONMENT` | `production` | Liga o modo de produção. |
| `ENABLE_DOCS` | `false` | Desabilita `/docs`, `/redoc` e `/openapi.json`. |
| `APP_NAME` | `MicroData Tools API` | |
| `APP_VERSION` | `0.1.0` | |
| `MAX_UPLOAD_SIZE_MB` | `10` | Limite de upload (leitura em chunks). |
| `BACKEND_CORS_ORIGINS` | `https://microdata-tools.vercel.app` | Lista separada por vírgula. |
| `RATE_LIMIT_ENABLED` | `true` | Liga o rate limit em memória. |
| `RATE_LIMIT_REQUESTS_PER_MINUTE` | `60` | Limite geral por IP. |
| `RATE_LIMIT_UPLOADS_PER_MINUTE` | `20` | Limite de uploads por IP. |
| `PYTHON_VERSION` | `3.12.3` | Usada pelo Render. |

Esses valores já estão declarados em `render.yaml`.

### Frontend (Vercel)

| Variável | Valor de produção | Observação |
| --- | --- | --- |
| `NEXT_PUBLIC_API_BASE_URL` | `https://microdata-tools-api.onrender.com` | **Obrigatória** e **precisa ser HTTPS**. O build falha sem ela. |

O guard em `frontend/next.config.ts` derruba o build de produção se a variável
estiver ausente ou não começar com `https://`. URLs HTTP só são aceitas em
desenvolvimento.

## Checklist de pré-deploy

- [ ] `main` está verde no CI (`.github/workflows/ci.yml`).
- [ ] Backend: `cd backend && uv run ruff check . && uv run pytest` passam local.
- [ ] Frontend: `cd frontend && npm run lint && npx tsc --noEmit && npm test` passam.
- [ ] `frontend/.env.local` **não** está versionado (apenas `.env.example`).
- [ ] Domínios definidos e consistentes entre `BACKEND_CORS_ORIGINS` e
      `NEXT_PUBLIC_API_BASE_URL`.
- [ ] Variáveis configuradas no Render e no Vercel.
- [ ] Confirmado que frontend e backend serão servidos via HTTPS.

## Deploy

### Backend (Render)

1. Conectar o repositório no Render usando o Blueprint (`render.yaml`).
2. Confirmar as variáveis de ambiente (ver tabela acima).
3. Build: `pip install uv && uv sync --frozen --no-dev`.
4. Start: `uv run fastapi run app/main.py --host 0.0.0.0 --port $PORT`.
5. Health check: `/health`.

### Frontend (Vercel)

1. Importar o projeto apontando o root para `frontend/`.
2. Definir `NEXT_PUBLIC_API_BASE_URL` (HTTPS) no ambiente de produção.
3. Build: `npm run build` (install via `npm ci`).

## Checklist de pós-deploy

- [ ] `GET https://<backend>/health` retorna `{"status":"ok"}`.
- [ ] `GET https://<backend>/docs` retorna **404** (docs desligadas em produção).
- [ ] Frontend carrega via HTTPS sem erros de CSP no console.
- [ ] Upload a partir do frontend funciona (sem erro de CORS).
- [ ] Download preserva o nome do arquivo (`Content-Disposition` exposto).
- [ ] Rate limit responde `429` ao exceder o limite de uploads.

### Validações manuais (smoke test)

Pelo frontend publicado, com um CSV de exemplo (ver `backend/samples/`):

- [ ] **/health** — backend responde ok.
- [ ] **Preview** — `/api/files/preview` mostra colunas e prévia.
- [ ] **Clean** — `/api/files/clean-preview` e `/api/files/clean-download`.
- [ ] **Convert** — `/api/files/convert-preview` e `/api/files/convert-download`
      (JSON, Markdown, SQL).
- [ ] **Analyze** — `/api/files/analyze-preview` retorna estatísticas.
- [ ] **Download** — o arquivo baixado abre e tem o nome esperado.
- [ ] **Limite** — arquivo acima de `MAX_UPLOAD_SIZE_MB` retorna `413`.

## Privacidade e logs

- Os arquivos são processados **em memória** e não são persistidos.
- Não há contas, sessões nem histórico de uploads.
- **Não** registrar o conteúdo dos arquivos enviados nos logs. Logar apenas
  metadados não sensíveis (status, latência, tamanho, endpoint).
- O rate limit guarda apenas IP + timestamps em memória, sem conteúdo.
- A CSP inicial mantém `unsafe-inline`; endurecer via nonce é melhoria posterior.
- Revisar a política de privacidade antes de divulgar o beta publicamente.
