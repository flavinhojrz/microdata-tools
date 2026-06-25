import pytest

from app.core.rate_limit import rate_limiter


@pytest.fixture(autouse=True)
def disable_rate_limit_by_default(monkeypatch):
    # A suíte dispara muitos uploads em sequência; com o limite ligado por padrão
    # os testes existentes bateriam em 429. Cada teste de rate limit liga o limite
    # explicitamente. Sempre limpamos o estado do limiter entre testes.
    monkeypatch.setenv("RATE_LIMIT_ENABLED", "false")
    rate_limiter.reset()
    yield
    rate_limiter.reset()
