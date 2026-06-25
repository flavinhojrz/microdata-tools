from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_upload_above_limit_returns_413(monkeypatch) -> None:
    monkeypatch.setenv("MAX_UPLOAD_SIZE_MB", "0")

    response = client.post(
        "/api/files/preview",
        files={"file": ("vendas.csv", b"produto,valor\nQueijo,10\n", "text/csv")},
    )

    assert response.status_code == 413
    assert (
        response.json()["detail"] == "Arquivo muito grande. O limite atual é de 0 MB."
    )


def test_upload_streamed_above_limit_returns_413(monkeypatch) -> None:
    monkeypatch.setenv("MAX_UPLOAD_SIZE_MB", "1")

    oversized = b"produto,valor\n" + (b"a" * (2 * 1024 * 1024))

    response = client.post(
        "/api/files/preview",
        files={"file": ("vendas.csv", oversized, "text/csv")},
    )

    assert response.status_code == 413
    assert (
        response.json()["detail"] == "Arquivo muito grande. O limite atual é de 1 MB."
    )


def test_upload_within_limit_still_works(monkeypatch) -> None:
    monkeypatch.setenv("MAX_UPLOAD_SIZE_MB", "1")

    response = client.post(
        "/api/files/preview",
        files={"file": ("vendas.csv", b"produto,valor\nQueijo,10\n", "text/csv")},
    )

    assert response.status_code == 200
    assert response.json()["rows_count"] == 1
