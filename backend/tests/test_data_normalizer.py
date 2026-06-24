import pandas as pd

from app.services.data_normalizer import (
    normalize_brazilian_dataframe,
    normalize_brazilian_date_columns,
    normalize_brazilian_number_value,
    normalize_brazilian_numeric_columns,
)


def test_normalize_brazilian_number_value_converts_decimal_comma() -> None:
    assert normalize_brazilian_number_value("30,50") == 30.5


def test_normalize_brazilian_number_value_converts_thousand_separator() -> None:
    assert normalize_brazilian_number_value("1.234,56") == 1234.56


def test_normalize_brazilian_number_value_converts_currency() -> None:
    assert normalize_brazilian_number_value("R$ 1.234,56") == 1234.56


def test_normalize_brazilian_number_value_converts_negative_value() -> None:
    assert normalize_brazilian_number_value("R$ -10,50") == -10.5
    assert normalize_brazilian_number_value("-10,50") == -10.5


def test_normalize_brazilian_number_value_preserves_non_numeric_text() -> None:
    assert normalize_brazilian_number_value("abc") == "abc"


def test_normalize_brazilian_number_value_preserves_numeric_value() -> None:
    assert normalize_brazilian_number_value(30.5) == 30.5


def test_normalize_brazilian_numeric_columns_converts_when_rate_reaches_threshold() -> (
    None
):
    dataframe = pd.DataFrame({"valor": ["R$ 1.234,56", "30,50", "12,00", None]})

    normalized_dataframe, normalized_columns = normalize_brazilian_numeric_columns(
        dataframe
    )

    assert normalized_columns == ["valor"]
    assert normalized_dataframe["valor"].tolist()[:3] == [1234.56, 30.5, 12.0]


def test_normalize_brazilian_numeric_columns_does_not_convert_below_threshold() -> None:
    dataframe = pd.DataFrame({"valor": ["30,50", "abc", "texto", None]})

    normalized_dataframe, normalized_columns = normalize_brazilian_numeric_columns(
        dataframe
    )

    assert normalized_columns == []
    pd.testing.assert_frame_equal(normalized_dataframe, dataframe)


def test_normalize_brazilian_date_columns_detects_clear_brazilian_dates() -> None:
    dataframe = pd.DataFrame({"data": ["01/06/2026", "31/12/2026", "2026-06-01", None]})

    normalized_dataframe, normalized_columns = normalize_brazilian_date_columns(
        dataframe
    )

    assert normalized_columns == ["data"]
    valid_dates = normalized_dataframe["data"].dropna()
    assert valid_dates.min().date().isoformat() == "2026-06-01"
    assert valid_dates.max().date().isoformat() == "2026-12-31"


def test_normalize_brazilian_date_columns_does_not_convert_below_threshold() -> None:
    dataframe = pd.DataFrame({"data": ["31/12/2026", "sem data", "texto", None]})

    normalized_dataframe, normalized_columns = normalize_brazilian_date_columns(
        dataframe
    )

    assert normalized_columns == []
    pd.testing.assert_frame_equal(normalized_dataframe, dataframe)


def test_normalize_brazilian_dataframe_returns_normalization_report() -> None:
    dataframe = pd.DataFrame(
        {
            "data": ["01/06/2026", "31/12/2026"],
            "valor": ["R$ 30,50", "1.234,56"],
        }
    )

    _, report = normalize_brazilian_dataframe(dataframe)

    assert report == {
        "numeric_columns_normalized": ["valor"],
        "date_columns_normalized": ["data"],
    }


def test_normalizer_functions_do_not_mutate_original_dataframe() -> None:
    dataframe = pd.DataFrame(
        {
            "data": ["01/06/2026", "31/12/2026"],
            "valor": ["R$ 30,50", "1.234,56"],
        }
    )
    original_dataframe = dataframe.copy(deep=True)

    normalize_brazilian_dataframe(dataframe)

    pd.testing.assert_frame_equal(dataframe, original_dataframe)
