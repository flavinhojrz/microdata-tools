from fastapi.testclient import TestClient

from app.main import create_app


def test_docs_disabled_in_production(monkeypatch) -> None:
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("ENABLE_DOCS", "false")

    client = TestClient(create_app())

    assert client.get("/docs").status_code == 404
    assert client.get("/redoc").status_code == 404
    assert client.get("/openapi.json").status_code == 404
    # O health check continua disponível mesmo com a documentação desligada.
    assert client.get("/health").status_code == 200


def test_docs_enabled_in_development(monkeypatch) -> None:
    monkeypatch.setenv("ENVIRONMENT", "development")
    monkeypatch.delenv("ENABLE_DOCS", raising=False)

    client = TestClient(create_app())

    assert client.get("/docs").status_code == 200
    assert client.get("/redoc").status_code == 200
    assert client.get("/openapi.json").status_code == 200
