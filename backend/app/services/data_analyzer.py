from collections.abc import Iterator
from typing import Any

import pandas as pd
from pandas.api.types import (
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
    is_string_dtype,
)


DATE_DETECTION_THRESHOLD = 0.8
MAX_TOP_VALUES = 5


def analyze_dataframe(dataframe: pd.DataFrame) -> dict[str, Any]:
    return {
        "rows_count": int(dataframe.shape[0]),
        "columns_count": int(dataframe.shape[1]),
        "columns": [str(column) for column in dataframe.columns],
        "missing_values_count": int(dataframe.isna().sum().sum()),
        "duplicate_rows_count": int(dataframe.duplicated().sum()),
        "empty_columns_count": int(dataframe.isna().all(axis=0).sum()),
        "column_summaries": build_column_summaries(dataframe),
        "numeric_summaries": build_numeric_summaries(dataframe),
        "categorical_summaries": build_categorical_summaries(dataframe),
        "date_summaries": build_date_summaries(dataframe),
    }


def build_column_summaries(dataframe: pd.DataFrame) -> list[dict[str, Any]]:
    rows_count = int(dataframe.shape[0])
    summaries: list[dict[str, Any]] = []

    for name, series in _iter_columns(dataframe):
        missing_count = int(series.isna().sum())
        missing_percentage = (
            round((missing_count / rows_count) * 100, 2) if rows_count > 0 else 0.0
        )

        summaries.append(
            {
                "name": name,
                "dtype": str(series.dtype),
                "missing_count": missing_count,
                "missing_percentage": missing_percentage,
                "unique_count": int(series.nunique(dropna=True)),
            }
        )

    return summaries


def build_numeric_summaries(dataframe: pd.DataFrame) -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []

    for name, series in _iter_columns(dataframe):
        if not is_numeric_dtype(series) or pd.api.types.is_bool_dtype(series):
            continue

        count = int(series.count())
        summaries.append(
            {
                "name": name,
                "count": count,
                "mean": _number_or_none(series.mean()) if count else None,
                "min": _number_or_none(series.min()) if count else None,
                "max": _number_or_none(series.max()) if count else None,
                "sum": _number_or_none(series.sum()) if count else None,
            }
        )

    return summaries


def build_categorical_summaries(dataframe: pd.DataFrame) -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []

    for name, series in _iter_columns(dataframe):
        if not _is_categorical_series(series):
            continue

        top_values = [
            {
                "value": str(value),
                "count": int(count),
            }
            for value, count in series.value_counts(dropna=True)
            .head(MAX_TOP_VALUES)
            .items()
        ]

        summaries.append(
            {
                "name": name,
                "unique_count": int(series.nunique(dropna=True)),
                "top_values": top_values,
            }
        )

    return summaries


def build_date_summaries(dataframe: pd.DataFrame) -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []

    for name, series in _iter_columns(dataframe):
        if not _is_potential_date_series(series):
            continue

        non_empty_values = _drop_empty_values(series)

        if non_empty_values.empty:
            continue

        if not is_datetime64_any_dtype(series) and not _has_date_like_values(
            non_empty_values
        ):
            continue

        converted_dates = pd.to_datetime(
            non_empty_values,
            errors="coerce",
            dayfirst=True,
        )
        valid_dates = converted_dates.dropna()

        if valid_dates.empty:
            continue

        valid_ratio = len(valid_dates) / len(non_empty_values)

        if valid_ratio < DATE_DETECTION_THRESHOLD:
            continue

        summaries.append(
            {
                "name": name,
                "min_date": valid_dates.min().date().isoformat(),
                "max_date": valid_dates.max().date().isoformat(),
                "valid_dates_count": int(len(valid_dates)),
            }
        )

    return summaries


def _iter_columns(dataframe: pd.DataFrame) -> Iterator[tuple[str, pd.Series]]:
    for index, column in enumerate(dataframe.columns):
        yield str(column), dataframe.iloc[:, index]


def _number_or_none(value: Any) -> float | None:
    if pd.isna(value):
        return None

    return float(value)


def _is_categorical_series(series: pd.Series) -> bool:
    return (
        is_object_dtype(series)
        or is_string_dtype(series)
        or isinstance(series.dtype, pd.CategoricalDtype)
    )


def _is_potential_date_series(series: pd.Series) -> bool:
    return is_datetime64_any_dtype(series) or _is_categorical_series(series)


def _drop_empty_values(series: pd.Series) -> pd.Series:
    non_null_values = series.dropna()

    if is_datetime64_any_dtype(series):
        return non_null_values

    return non_null_values[non_null_values.astype(str).str.strip() != ""]


def _has_date_like_values(series: pd.Series) -> bool:
    string_values = series.astype(str).str.strip()
    values_with_digits_count = int(string_values.str.contains(r"\d", regex=True).sum())
    return values_with_digits_count / len(string_values) >= DATE_DETECTION_THRESHOLD
