import pandas as pd

from app.services.data_cleaner import (
    clean_dataframe,
    normalize_column_name,
    normalize_column_names,
)


def test_clean_dataframe_removes_fully_empty_rows() -> None:
    dataframe = pd.DataFrame(
        {
            "name": ["Ana", None, "Bia"],
            "value": [10, None, 20],
        }
    )

    cleaned_dataframe, report = clean_dataframe(dataframe)

    assert len(cleaned_dataframe) == 2
    assert report["removed_empty_rows_count"] == 1
    assert report["cleaned_rows_count"] == 2


def test_clean_dataframe_removes_fully_empty_columns() -> None:
    dataframe = pd.DataFrame(
        {
            "name": ["Ana", "Bia"],
            "empty": [None, None],
        }
    )

    cleaned_dataframe, report = clean_dataframe(dataframe)

    assert list(cleaned_dataframe.columns) == ["name"]
    assert report["removed_empty_columns_count"] == 1
    assert report["cleaned_columns_count"] == 1


def test_clean_dataframe_removes_duplicate_rows() -> None:
    dataframe = pd.DataFrame(
        {
            "name": ["Ana", "Ana", "Bia"],
            "value": [10, 10, 20],
        }
    )

    cleaned_dataframe, report = clean_dataframe(dataframe)

    assert cleaned_dataframe.to_dict(orient="records") == [
        {"name": "Ana", "value": 10},
        {"name": "Bia", "value": 20},
    ]
    assert report["removed_duplicate_rows_count"] == 1


def test_normalize_column_name_with_spaces() -> None:
    assert normalize_column_name(" Data Venda ") == "data_venda"


def test_normalize_column_name_with_accents() -> None:
    assert normalize_column_name("Observação") == "observacao"


def test_normalize_column_name_with_special_characters() -> None:
    assert normalize_column_name("Valor R$") == "valor_r"


def test_normalize_column_names_resolves_duplicates_after_normalization() -> None:
    columns = [
        " Data Venda ",
        "Forma de Pagamento",
        "Valor R$",
        "Observação",
        "Observação",
    ]

    assert normalize_column_names(columns) == [
        "data_venda",
        "forma_de_pagamento",
        "valor_r",
        "observacao",
        "observacao_2",
    ]


def test_clean_dataframe_preserves_cell_values() -> None:
    dataframe = pd.DataFrame(
        {
            " Customer ": ["  Ana  ", "Bia"],
            "Valor R$": ["R$ 1.234,50", "R$ 2.000,00"],
        }
    )

    cleaned_dataframe, _ = clean_dataframe(dataframe)

    assert cleaned_dataframe.to_dict(orient="records") == [
        {"customer": "  Ana  ", "valor_r": "R$ 1.234,50"},
        {"customer": "Bia", "valor_r": "R$ 2.000,00"},
    ]
