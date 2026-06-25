from fastapi.testclient import TestClient

from app.core.rate_limit import rate_limiter
from app.main import create_app


CSV_BYTES = b"produto,valor\nQueijo,10\n"


def _upload(client: TestClient):
    return client.post(
        "/api/files/preview",
        files={"file": ("vendas.csv", CSV_BYTES, "text/csv")},
    )


def test_upload_endpoint_returns_429_when_limit_exceeded(monkeypatch) -> None:
    monkeypatch.setenv("RATE_LIMIT_ENABLED", "true")
    monkeypatch.setenv("RATE_LIMIT_UPLOADS_PER_MINUTE", "2")
    monkeypatch.setenv("RATE_LIMIT_REQUESTS_PER_MINUTE", "60")
    rate_limiter.reset()

    client = TestClient(create_app())

    assert _upload(client).status_code == 200
    assert _upload(client).status_code == 200

    blocked = _upload(client)

    assert blocked.status_code == 429
    assert "Muitas requisições" in blocked.json()["detail"]
    assert blocked.headers["retry-after"] == "60"


def test_health_is_not_rate_limited(monkeypatch) -> None:
    monkeypatch.setenv("RATE_LIMIT_ENABLED", "true")
    monkeypatch.setenv("RATE_LIMIT_UPLOADS_PER_MINUTE", "1")
    monkeypatch.setenv("RATE_LIMIT_REQUESTS_PER_MINUTE", "1")
    rate_limiter.reset()

    client = TestClient(create_app())

    for _ in range(5):
        assert client.get("/health").status_code == 200


def test_rate_limit_disabled_allows_many_uploads(monkeypatch) -> None:
    monkeypatch.setenv("RATE_LIMIT_ENABLED", "false")
    monkeypatch.setenv("RATE_LIMIT_UPLOADS_PER_MINUTE", "1")
    rate_limiter.reset()

    client = TestClient(create_app())

    for _ in range(5):
        assert _upload(client).status_code == 200
