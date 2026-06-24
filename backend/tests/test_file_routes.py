import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)

DIRTY_CSV = """ Data Venda ,Forma de Pagamento,Valor R$,Observação,Coluna Vazia
2026-06-01,Pix,"R$ 120,00",Pago,
2026-06-01,Pix,"R$ 120,00",Pago,
,,,,
2026-06-02,Cartão,"R$ 250,00",Aguardando,
"""

ANALYSIS_CSV = """Data Venda,Produto,Forma Pagamento,Valor,Observação
01/06/2026,Queijo,Pix,30.5,Pago
02/06/2026,Café,Cartão,20.0,
02/06/2026,Café,Cartão,20.0,
,Queijo,Pix,10.0,
"""


def test_clean_download_file_returns_csv_download() -> None:
    response = client.post(
        "/api/files/clean-download",
        files={"file": ("vendas-sujas.csv", DIRTY_CSV.encode(), "text/csv")},
    )

    csv_text = response.content.decode("utf-8-sig")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")
    assert (
        response.headers["content-disposition"]
        == 'attachment; filename="vendas-sujas_clean.csv"'
    )
    assert "data_venda,forma_de_pagamento,valor_r,observacao" in csv_text
    assert "coluna_vazia" not in csv_text
    assert csv_text.count("2026-06-01") == 1
    assert "R$ 120,00" in csv_text


def test_preview_file_still_responds() -> None:
    response = client.post(
        "/api/files/preview",
        files={"file": ("vendas-sujas.csv", DIRTY_CSV.encode(), "text/csv")},
    )

    assert response.status_code == 200
    assert response.json()["columns_count"] == 5


def test_clean_preview_file_still_responds() -> None:
    response = client.post(
        "/api/files/clean-preview",
        files={"file": ("vendas-sujas.csv", DIRTY_CSV.encode(), "text/csv")},
    )

    body = response.json()

    assert response.status_code == 200
    assert body["cleaned_columns"] == [
        "data_venda",
        "forma_de_pagamento",
        "valor_r",
        "observacao",
    ]


def test_convert_preview_file_with_json_returns_preview() -> None:
    response = client.post(
        "/api/files/convert-preview",
        data={"target_format": "json"},
        files={"file": ("vendas-sujas.csv", DIRTY_CSV.encode(), "text/csv")},
    )

    body = response.json()

    assert response.status_code == 200
    assert body["target_format"] == "json"
    assert body["clean_before_convert"] is True
    assert '"data_venda"' in body["content_preview"]


def test_convert_preview_file_with_markdown_returns_preview() -> None:
    response = client.post(
        "/api/files/convert-preview",
        data={"target_format": "markdown"},
        files={"file": ("vendas-sujas.csv", DIRTY_CSV.encode(), "text/csv")},
    )

    body = response.json()

    assert response.status_code == 200
    assert (
        "| data_venda | forma_de_pagamento | valor_r | observacao |"
        in body["content_preview"]
    )


def test_convert_preview_file_with_sql_returns_preview() -> None:
    response = client.post(
        "/api/files/convert-preview",
        data={"target_format": "sql", "table_name": "vendas"},
        files={"file": ("vendas-sujas.csv", DIRTY_CSV.encode(), "text/csv")},
    )

    body = response.json()

    assert response.status_code == 200
    assert "INSERT INTO vendas" in body["content_preview"]


@pytest.mark.parametrize(
    ("target_format", "expected_content_type", "expected_filename"),
    [
        ("json", "application/json", "vendas-sujas_clean.json"),
        ("markdown", "text/markdown", "vendas-sujas_clean.md"),
        ("sql", "application/sql", "vendas-sujas_clean.sql"),
    ],
)
def test_convert_download_file_returns_download(
    target_format: str,
    expected_content_type: str,
    expected_filename: str,
) -> None:
    response = client.post(
        "/api/files/convert-download",
        data={"target_format": target_format, "table_name": "vendas"},
        files={"file": ("vendas-sujas.csv", DIRTY_CSV.encode(), "text/csv")},
    )

    assert response.status_code == 200
    assert response.headers["content-type"].startswith(expected_content_type)
    assert (
        response.headers["content-disposition"]
        == f'attachment; filename="{expected_filename}"'
    )


def test_convert_preview_file_with_invalid_format_returns_400() -> None:
    response = client.post(
        "/api/files/convert-preview",
        data={"target_format": "xml"},
        files={"file": ("vendas-sujas.csv", DIRTY_CSV.encode(), "text/csv")},
    )

    assert response.status_code == 400


def test_analyze_preview_file_returns_analysis_with_cleaning_enabled() -> None:
    response = client.post(
        "/api/files/analyze-preview",
        data={"clean_before_analyze": "true"},
        files={"file": ("vendas-analise.csv", ANALYSIS_CSV.encode(), "text/csv")},
    )

    body = response.json()

    assert response.status_code == 200
    assert body["clean_before_analyze"] is True
    assert body["rows_count"] == 3
    assert body["columns_count"] == 5
    assert body["column_summaries"]
    assert body["numeric_summaries"]
    assert body["categorical_summaries"]
    assert body["date_summaries"]


def test_analyze_preview_file_returns_analysis_without_cleaning() -> None:
    response = client.post(
        "/api/files/analyze-preview",
        data={"clean_before_analyze": "false"},
        files={"file": ("vendas-analise.csv", ANALYSIS_CSV.encode(), "text/csv")},
    )

    body = response.json()

    assert response.status_code == 200
    assert body["clean_before_analyze"] is False
    assert body["rows_count"] == 4
    assert body["duplicate_rows_count"] == 1
