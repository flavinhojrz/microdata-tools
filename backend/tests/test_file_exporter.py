import pandas as pd

from app.services.file_exporter import (
    build_cleaned_filename,
    dataframe_to_csv_bytes,
)


def test_build_cleaned_filename_for_csv() -> None:
    assert build_cleaned_filename("vendas.csv") == "vendas_clean.csv"


def test_build_cleaned_filename_for_excel() -> None:
    assert build_cleaned_filename("relatorio.xlsx") == "relatorio_clean.csv"


def test_build_cleaned_filename_for_empty_filename() -> None:
    assert build_cleaned_filename("") == "arquivo_limpo.csv"


def test_dataframe_to_csv_bytes_returns_bytes() -> None:
    dataframe = pd.DataFrame({"data_venda": ["2026-06-01"]})

    csv_bytes = dataframe_to_csv_bytes(dataframe)

    assert isinstance(csv_bytes, bytes)


def test_dataframe_to_csv_bytes_does_not_include_index() -> None:
    dataframe = pd.DataFrame(
        {"data_venda": ["2026-06-01"]},
        index=[99],
    )

    csv_text = dataframe_to_csv_bytes(dataframe).decode("utf-8-sig")

    assert csv_text.splitlines() == [
        "data_venda",
        "2026-06-01",
    ]


def test_dataframe_to_csv_bytes_contains_cleaned_column_names() -> None:
    dataframe = pd.DataFrame(
        {
            "data_venda": ["2026-06-01"],
            "valor_r": ["R$ 120,00"],
        }
    )

    csv_text = dataframe_to_csv_bytes(dataframe).decode("utf-8-sig")

    assert csv_text.splitlines()[0] == "data_venda,valor_r"
