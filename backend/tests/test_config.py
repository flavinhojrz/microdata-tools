from app.core.config import BYTES_PER_MEGABYTE, Settings


def test_cors_origins_parses_comma_separated_string(monkeypatch) -> None:
    monkeypatch.setenv(
        "BACKEND_CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    )

    settings = Settings()

    assert settings.cors_origins == [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]


def test_cors_origins_removes_spaces_and_empty_values(monkeypatch) -> None:
    monkeypatch.setenv(
        "BACKEND_CORS_ORIGINS",
        " http://localhost:5173, , http://127.0.0.1:5173,, ",
    )

    settings = Settings()

    assert settings.cors_origins == [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]


def test_max_upload_size_bytes_converts_mb_to_bytes(monkeypatch) -> None:
    monkeypatch.setenv("MAX_UPLOAD_SIZE_MB", "2")

    settings = Settings()

    assert settings.max_upload_size_bytes == 2 * BYTES_PER_MEGABYTE


def test_environment_defaults_to_development(monkeypatch) -> None:
    monkeypatch.delenv("ENVIRONMENT", raising=False)

    settings = Settings()

    assert settings.ENVIRONMENT == "development"
    assert settings.is_production is False


def test_is_production_when_environment_is_production(monkeypatch) -> None:
    monkeypatch.setenv("ENVIRONMENT", "Production")

    settings = Settings()

    assert settings.is_production is True


def test_docs_disabled_by_default_in_production(monkeypatch) -> None:
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.delenv("ENABLE_DOCS", raising=False)

    settings = Settings()

    assert settings.ENABLE_DOCS is False


def test_docs_enabled_by_default_in_development(monkeypatch) -> None:
    monkeypatch.setenv("ENVIRONMENT", "development")
    monkeypatch.delenv("ENABLE_DOCS", raising=False)

    settings = Settings()

    assert settings.ENABLE_DOCS is True


def test_enable_docs_env_overrides_default(monkeypatch) -> None:
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("ENABLE_DOCS", "true")

    settings = Settings()

    assert settings.ENABLE_DOCS is True


def test_rate_limit_settings_parse_from_env(monkeypatch) -> None:
    monkeypatch.setenv("RATE_LIMIT_ENABLED", "false")
    monkeypatch.setenv("RATE_LIMIT_REQUESTS_PER_MINUTE", "120")
    monkeypatch.setenv("RATE_LIMIT_UPLOADS_PER_MINUTE", "30")

    settings = Settings()

    assert settings.RATE_LIMIT_ENABLED is False
    assert settings.RATE_LIMIT_REQUESTS_PER_MINUTE == 120
    assert settings.RATE_LIMIT_UPLOADS_PER_MINUTE == 30


def test_rate_limit_defaults(monkeypatch) -> None:
    monkeypatch.delenv("RATE_LIMIT_ENABLED", raising=False)
    monkeypatch.delenv("RATE_LIMIT_REQUESTS_PER_MINUTE", raising=False)
    monkeypatch.delenv("RATE_LIMIT_UPLOADS_PER_MINUTE", raising=False)

    settings = Settings()

    assert settings.RATE_LIMIT_ENABLED is True
    assert settings.RATE_LIMIT_REQUESTS_PER_MINUTE == 60
    assert settings.RATE_LIMIT_UPLOADS_PER_MINUTE == 20
