import json

import pandas as pd
import pytest

from app.services.data_converter import (
    build_converted_filename,
    dataframe_to_json_string,
    dataframe_to_markdown_string,
    dataframe_to_sql_insert_string,
    validate_target_format,
)


def test_validate_target_format_accepts_json() -> None:
    assert validate_target_format("json") == "json"


def test_validate_target_format_normalizes_value() -> None:
    assert validate_target_format(" JSON ") == "json"


def test_validate_target_format_rejects_invalid_format() -> None:
    with pytest.raises(ValueError, match="Formato de destino inválido"):
        validate_target_format("xml")


def test_dataframe_to_json_string_generates_list_of_objects() -> None:
    dataframe = pd.DataFrame(
        {
            "data_venda": ["2026-06-01"],
            "produto": ["Queijo"],
        }
    )

    json_text = dataframe_to_json_string(dataframe)

    assert json.loads(json_text) == [
        {
            "data_venda": "2026-06-01",
            "produto": "Queijo",
        }
    ]


def test_dataframe_to_json_string_preserves_accents() -> None:
    dataframe = pd.DataFrame({"produto": ["Café"]})

    json_text = dataframe_to_json_string(dataframe)

    assert "Café" in json_text


def test_dataframe_to_markdown_string_does_not_include_index() -> None:
    dataframe = pd.DataFrame(
        {"produto": ["Queijo"]},
        index=[99],
    )

    markdown = dataframe_to_markdown_string(dataframe)

    assert "99" not in markdown


def test_dataframe_to_markdown_string_contains_column_names() -> None:
    dataframe = pd.DataFrame(
        {
            "data_venda": ["2026-06-01"],
            "produto": ["Queijo"],
        }
    )

    markdown = dataframe_to_markdown_string(dataframe)

    assert "| data_venda | produto |" in markdown


def test_dataframe_to_sql_insert_string_generates_insert_into() -> None:
    dataframe = pd.DataFrame({"produto": ["Queijo"]})

    sql = dataframe_to_sql_insert_string(dataframe, table_name="vendas")

    assert sql == "INSERT INTO vendas (produto) VALUES ('Queijo');"


def test_dataframe_to_sql_insert_string_escapes_single_quotes() -> None:
    dataframe = pd.DataFrame({"editora": ["O'Reilly"]})

    sql = dataframe_to_sql_insert_string(dataframe)

    assert "'O''Reilly'" in sql


def test_dataframe_to_sql_insert_string_turns_missing_values_into_null() -> None:
    dataframe = pd.DataFrame({"produto": [None]})

    sql = dataframe_to_sql_insert_string(dataframe)

    assert "VALUES (NULL);" in sql


def test_dataframe_to_sql_insert_string_keeps_numbers_unquoted() -> None:
    dataframe = pd.DataFrame({"valor": [30.5]})

    sql = dataframe_to_sql_insert_string(dataframe)

    assert "VALUES (30.5);" in sql


def test_build_converted_filename_for_clean_json() -> None:
    assert build_converted_filename("vendas.csv", "json", cleaned=True) == (
        "vendas_clean.json"
    )


def test_build_converted_filename_for_uncleaned_json() -> None:
    assert build_converted_filename("vendas.csv", "json", cleaned=False) == (
        "vendas.json"
    )


def test_build_converted_filename_for_clean_sql_from_excel() -> None:
    assert build_converted_filename("relatorio.xlsx", "sql", cleaned=True) == (
        "relatorio_clean.sql"
    )


def test_build_converted_filename_for_empty_markdown_filename() -> None:
    assert build_converted_filename("", "markdown", cleaned=False) == "dados.md"
