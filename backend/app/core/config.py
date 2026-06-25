import os


DEFAULT_APP_NAME = "MicroData Tools API"
DEFAULT_APP_VERSION = "0.1.0"
DEFAULT_APP_DESCRIPTION = "API para limpar, converter e analisar arquivos CSV e Excel."
DEFAULT_BACKEND_CORS_ORIGINS = "http://localhost:3000,http://127.0.0.1:3000"
DEFAULT_MAX_UPLOAD_SIZE_MB = 10
DEFAULT_ENVIRONMENT = "development"
PRODUCTION_ENVIRONMENT = "production"
DEFAULT_RATE_LIMIT_REQUESTS_PER_MINUTE = 60
DEFAULT_RATE_LIMIT_UPLOADS_PER_MINUTE = 20
BYTES_PER_MEGABYTE = 1024 * 1024


class Settings:
    def __init__(self) -> None:
        self.APP_NAME = os.getenv("APP_NAME", DEFAULT_APP_NAME)
        self.APP_VERSION = os.getenv("APP_VERSION", DEFAULT_APP_VERSION)
        self.APP_DESCRIPTION = os.getenv("APP_DESCRIPTION", DEFAULT_APP_DESCRIPTION)
        self.BACKEND_CORS_ORIGINS = os.getenv(
            "BACKEND_CORS_ORIGINS",
            DEFAULT_BACKEND_CORS_ORIGINS,
        )
        self.MAX_UPLOAD_SIZE_MB = _get_int_env(
            "MAX_UPLOAD_SIZE_MB",
            DEFAULT_MAX_UPLOAD_SIZE_MB,
        )
        self.ENVIRONMENT = os.getenv("ENVIRONMENT", DEFAULT_ENVIRONMENT).strip().lower()
        # Em produção a documentação interativa fica desligada por padrão para não
        # expor a superfície da API publicamente; em dev fica ligada para facilitar.
        self.ENABLE_DOCS = _get_bool_env("ENABLE_DOCS", default=not self.is_production)
        self.RATE_LIMIT_ENABLED = _get_bool_env("RATE_LIMIT_ENABLED", default=True)
        self.RATE_LIMIT_REQUESTS_PER_MINUTE = _get_int_env(
            "RATE_LIMIT_REQUESTS_PER_MINUTE",
            DEFAULT_RATE_LIMIT_REQUESTS_PER_MINUTE,
        )
        self.RATE_LIMIT_UPLOADS_PER_MINUTE = _get_int_env(
            "RATE_LIMIT_UPLOADS_PER_MINUTE",
            DEFAULT_RATE_LIMIT_UPLOADS_PER_MINUTE,
        )

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == PRODUCTION_ENVIRONMENT

    @property
    def cors_origins(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.BACKEND_CORS_ORIGINS.split(",")
            if origin.strip()
        ]

    @property
    def max_upload_size_bytes(self) -> int:
        return self.MAX_UPLOAD_SIZE_MB * BYTES_PER_MEGABYTE


def get_settings() -> Settings:
    return Settings()


def _get_int_env(name: str, default: int) -> int:
    value = os.getenv(name)

    if value is None:
        return default

    try:
        return int(value)
    except ValueError:
        return default


def _get_bool_env(name: str, default: bool) -> bool:
    value = os.getenv(name)

    if value is None:
        return default

    return value.strip().lower() in {"1", "true", "yes", "on"}


settings = get_settings()
