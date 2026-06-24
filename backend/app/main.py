from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(
    title="MicroData Tools API",
    description="API para limpar, converter e analisar arquivos CSV e Excel.",
    version="0.1.0",
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "MicroData Tools API",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
    }
