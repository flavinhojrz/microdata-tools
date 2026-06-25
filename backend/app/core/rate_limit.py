import time
from collections import defaultdict, deque
from threading import Lock

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.core.config import get_settings


WINDOW_SECONDS = 60
RATE_LIMITED_PREFIX = "/api/files/"


class InMemoryRateLimiter:
    """Rate limit por IP com janela deslizante guardada apenas em memória.

    Suficiente para o beta (instância única). Para múltiplas réplicas seria
    necessário um backend compartilhado, como Redis.
    """

    def __init__(self) -> None:
        self._hits: dict[str, deque[float]] = defaultdict(deque)
        self._lock = Lock()

    def is_allowed(self, key: str, limit: int, now: float | None = None) -> bool:
        if limit <= 0:
            return False

        timestamp = time.monotonic() if now is None else now
        cutoff = timestamp - WINDOW_SECONDS

        with self._lock:
            hits = self._hits[key]

            while hits and hits[0] <= cutoff:
                hits.popleft()

            if len(hits) >= limit:
                return False

            hits.append(timestamp)
            return True

    def reset(self) -> None:
        with self._lock:
            self._hits.clear()


rate_limiter = InMemoryRateLimiter()


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limiter: InMemoryRateLimiter | None = None) -> None:
        super().__init__(app)
        self._limiter = limiter or rate_limiter

    async def dispatch(self, request: Request, call_next):
        settings = get_settings()

        if not settings.RATE_LIMIT_ENABLED:
            return await call_next(request)

        # Só os endpoints de upload são limitados; /health e a raiz ficam livres.
        if not request.url.path.startswith(RATE_LIMITED_PREFIX):
            return await call_next(request)

        client_ip = _client_ip(request)

        general_ok = self._limiter.is_allowed(
            f"general:{client_ip}",
            settings.RATE_LIMIT_REQUESTS_PER_MINUTE,
        )
        upload_ok = self._limiter.is_allowed(
            f"upload:{client_ip}",
            settings.RATE_LIMIT_UPLOADS_PER_MINUTE,
        )

        if not general_ok or not upload_ok:
            return _too_many_requests()

        return await call_next(request)


def _too_many_requests() -> JSONResponse:
    return JSONResponse(
        status_code=429,
        content={
            "detail": (
                "Muitas requisições em pouco tempo. "
                "Aguarde um minuto e tente novamente."
            )
        },
        headers={"Retry-After": str(WINDOW_SECONDS)},
    )


def _client_ip(request: Request) -> str:
    # Atrás de um proxy (Render) o IP real vem no X-Forwarded-For; usamos o
    # primeiro endereço da cadeia. Sem proxy, caímos no host da conexão.
    forwarded = request.headers.get("x-forwarded-for")

    if forwarded:
        return forwarded.split(",")[0].strip()

    if request.client:
        return request.client.host

    return "unknown"
