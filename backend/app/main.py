from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.config import get_settings
from app.core.rate_limit import RateLimitMiddleware


def create_app() -> FastAPI:
    settings = get_settings()

    # Em produção (ENABLE_DOCS=false) /docs, /redoc e /openapi.json ficam
    # indisponíveis: passamos None para o FastAPI não montar essas rotas.
    docs_enabled = settings.ENABLE_DOCS

    app = FastAPI(
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION,
        docs_url="/docs" if docs_enabled else None,
        redoc_url="/redoc" if docs_enabled else None,
        openapi_url="/openapi.json" if docs_enabled else None,
    )

    # Ordem importa: o rate limit é adicionado antes do CORS para que o CORS
    # fique na camada externa e as respostas 429 também recebam os headers
    # cross-origin (e o preflight OPTIONS não seja contabilizado).
    app.add_middleware(RateLimitMiddleware)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        # Sem isto o navegador esconde o Content-Disposition em respostas
        # cross-origin, e o frontend não consegue ler o filename dos downloads.
        expose_headers=["Content-Disposition"],
    )

    app.include_router(router)

    @app.get("/")
    def root():
        return {
            "message": settings.APP_NAME,
            "status": "running",
        }

    @app.get("/health")
    def health_check():
        return {
            "status": "ok",
        }

    return app


app = create_app()
