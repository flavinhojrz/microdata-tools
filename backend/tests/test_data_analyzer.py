import pandas as pd

from app.services.data_analyzer import (
    analyze_dataframe,
    build_categorical_summaries,
    build_column_summaries,
    build_date_summaries,
    build_numeric_summaries,
)


def test_analyze_dataframe_returns_rows_and_columns_count() -> None:
    dataframe = pd.DataFrame(
        {
            "produto": ["Queijo", "Café"],
            "valor": [30.5, 20.0],
        }
    )

    analysis = analyze_dataframe(dataframe)

    assert analysis["rows_count"] == 2
    assert analysis["columns_count"] == 2


def test_analyze_dataframe_detects_missing_values() -> None:
    dataframe = pd.DataFrame({"produto": ["Queijo", None]})

    analysis = analyze_dataframe(dataframe)

    assert analysis["missing_values_count"] == 1


def test_analyze_dataframe_detects_duplicate_rows() -> None:
    dataframe = pd.DataFrame(
        {
            "produto": ["Queijo", "Queijo", "Café"],
            "valor": [30.5, 30.5, 20.0],
        }
    )

    analysis = analyze_dataframe(dataframe)

    assert analysis["duplicate_rows_count"] == 1


def test_analyze_dataframe_detects_empty_columns() -> None:
    dataframe = pd.DataFrame(
        {
            "produto": ["Queijo", "Café"],
            "vazia": [None, None],
        }
    )

    analysis = analyze_dataframe(dataframe)

    assert analysis["empty_columns_count"] == 1


def test_build_column_summaries_returns_missing_percentage_and_unique_count() -> None:
    dataframe = pd.DataFrame({"produto": ["Queijo", "Café", None, "Queijo"]})

    summaries = build_column_summaries(dataframe)

    assert summaries[0]["name"] == "produto"
    assert isinstance(summaries[0]["dtype"], str)
    assert summaries[0]["missing_count"] == 1
    assert summaries[0]["missing_percentage"] == 25.0
    assert summaries[0]["unique_count"] == 2


def test_build_numeric_summaries_returns_numeric_stats() -> None:
    dataframe = pd.DataFrame({"valor": [10.0, 20.0, 30.0, None]})

    summaries = build_numeric_summaries(dataframe)

    assert summaries == [
        {
            "name": "valor",
            "count": 3,
            "mean": 20.0,
            "min": 10.0,
            "max": 30.0,
            "sum": 60.0,
        }
    ]


def test_build_numeric_summaries_ignores_text_columns() -> None:
    dataframe = pd.DataFrame(
        {
            "valor": ["30,50", "20,00"],
            "produto": ["Queijo", "Café"],
        }
    )

    summaries = build_numeric_summaries(dataframe)

    assert summaries == []


def test_build_categorical_summaries_returns_top_values() -> None:
    dataframe = pd.DataFrame(
        {
            "produto": ["Queijo", "Café", "Queijo", None, "Café", "Queijo"],
        }
    )

    summaries = build_categorical_summaries(dataframe)

    assert summaries[0]["name"] == "produto"
    assert summaries[0]["unique_count"] == 2
    assert summaries[0]["top_values"][0] == {"value": "Queijo", "count": 3}


def test_build_date_summaries_detects_brazilian_dates() -> None:
    dataframe = pd.DataFrame(
        {
            "data_venda": ["01/06/2026", "02/06/2026", None, "15/06/2026"],
        }
    )

    summaries = build_date_summaries(dataframe)

    assert summaries == [
        {
            "name": "data_venda",
            "min_date": "2026-06-01",
            "max_date": "2026-06-15",
            "valid_dates_count": 3,
        }
    ]


def test_build_date_summaries_ignores_columns_with_low_valid_date_rate() -> None:
    dataframe = pd.DataFrame(
        {
            "observacao": ["01/06/2026", "sem data", "texto", None],
        }
    )

    summaries = build_date_summaries(dataframe)

    assert summaries == []


def test_analyzer_functions_do_not_mutate_original_dataframe() -> None:
    dataframe = pd.DataFrame(
        {
            "data_venda": ["01/06/2026", "02/06/2026"],
            "produto": ["Queijo", "Café"],
            "valor": [30.5, 20.0],
        }
    )
    original_dataframe = dataframe.copy(deep=True)

    analyze_dataframe(dataframe)

    pd.testing.assert_frame_equal(dataframe, original_dataframe)
