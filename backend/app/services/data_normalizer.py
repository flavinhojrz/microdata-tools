import re
from numbers import Number
from typing import Any

import pandas as pd
from pandas.api.types import is_bool_dtype, is_datetime64_any_dtype, is_numeric_dtype


DEFAULT_NORMALIZATION_THRESHOLD = 0.8
BRAZILIAN_NUMBER_PATTERN = re.compile(r"^[+-]?(?:\d+|\d{1,3}(?:\.\d{3})+)(?:,\d+)?$")


def normalize_brazilian_number_value(value: object) -> object:
    if _is_missing_value(value):
        return value

    if _is_number(value):
        return value

    if not isinstance(value, str):
        return value

    normalized_text = _prepare_brazilian_number_text(value)

    if not normalized_text:
        return value

    if not BRAZILIAN_NUMBER_PATTERN.fullmatch(normalized_text):
        return value

    normalized_text = normalized_text.replace(".", "").replace(",", ".")

    try:
        return float(normalized_text)
    except ValueError:
        return value


def normalize_brazilian_numeric_columns(
    dataframe: pd.DataFrame,
    threshold: float = DEFAULT_NORMALIZATION_THRESHOLD,
) -> tuple[pd.DataFrame, list[str]]:
    normalized_dataframe = dataframe.copy()
    normalized_columns: list[str] = []

    for index, column in enumerate(dataframe.columns):
        series = dataframe.iloc[:, index]

        if is_numeric_dtype(series) or is_bool_dtype(series):
            continue

        non_empty_values = _drop_empty_values(series)

        if non_empty_values.empty:
            continue

        converted_values = non_empty_values.map(normalize_brazilian_number_value)
        convertible_count = int(converted_values.map(_is_number).sum())
        conversion_rate = convertible_count / len(non_empty_values)

        if conversion_rate < threshold:
            continue

        normalized_dataframe.isetitem(index, _build_numeric_series(series))
        normalized_columns.append(str(column))

    return normalized_dataframe, normalized_columns


def normalize_brazilian_date_columns(
    dataframe: pd.DataFrame,
    threshold: float = DEFAULT_NORMALIZATION_THRESHOLD,
) -> tuple[pd.DataFrame, list[str]]:
    normalized_dataframe = dataframe.copy()
    normalized_columns: list[str] = []

    for index, column in enumerate(dataframe.columns):
        series = normalized_dataframe.iloc[:, index]

        if (
            is_datetime64_any_dtype(series)
            or is_numeric_dtype(series)
            or is_bool_dtype(series)
        ):
            continue

        non_empty_values = _drop_empty_values(series)

        if non_empty_values.empty:
            continue

        converted_dates = _to_datetime(non_empty_values)
        valid_dates_count = int(converted_dates.notna().sum())
        conversion_rate = valid_dates_count / len(non_empty_values)

        if conversion_rate < threshold:
            continue

        normalized_dataframe.isetitem(index, _to_datetime(series))
        normalized_columns.append(str(column))

    return normalized_dataframe, normalized_columns


def normalize_brazilian_dataframe(
    dataframe: pd.DataFrame,
) -> tuple[pd.DataFrame, dict[str, list[str]]]:
    normalized_dataframe, numeric_columns = normalize_brazilian_numeric_columns(
        dataframe
    )
    normalized_dataframe, date_columns = normalize_brazilian_date_columns(
        normalized_dataframe
    )

    return normalized_dataframe, {
        "numeric_columns_normalized": numeric_columns,
        "date_columns_normalized": date_columns,
    }


def _prepare_brazilian_number_text(value: str) -> str:
    text = value.strip()
    text = re.sub(r"(?i)r\$", "", text)
    return re.sub(r"\s+", "", text)


def _build_numeric_series(series: pd.Series) -> pd.Series:
    converted_values = series.map(_normalize_to_numeric_or_missing)
    return pd.to_numeric(converted_values, errors="coerce")


def _normalize_to_numeric_or_missing(value: object) -> object:
    if _is_empty_value(value):
        return pd.NA

    normalized_value = normalize_brazilian_number_value(value)

    if _is_number(normalized_value):
        return normalized_value

    return pd.NA


def _to_datetime(series: pd.Series) -> pd.Series:
    string_values = series.astype(str).str.strip()
    iso_date_mask = string_values.str.match(r"^\d{4}-\d{2}-\d{2}(?:\D|$)")
    converted_dates = pd.Series(pd.NaT, index=series.index, dtype="datetime64[ns]")

    if iso_date_mask.any():
        converted_dates.loc[iso_date_mask] = pd.to_datetime(
            series.loc[iso_date_mask],
            errors="coerce",
            format="%Y-%m-%d",
        )

    non_iso_mask = ~iso_date_mask

    if non_iso_mask.any():
        converted_dates.loc[non_iso_mask] = pd.to_datetime(
            series.loc[non_iso_mask],
            errors="coerce",
            dayfirst=True,
            format="mixed",
        )

    return converted_dates


def _drop_empty_values(series: pd.Series) -> pd.Series:
    non_null_values = series.dropna()

    return non_null_values[non_null_values.astype(str).str.strip() != ""]


def _is_empty_value(value: object) -> bool:
    if _is_missing_value(value):
        return True

    return isinstance(value, str) and value.strip() == ""


def _is_missing_value(value: object) -> bool:
    try:
        return bool(pd.isna(value))
    except (TypeError, ValueError):
        return False


def _is_number(value: Any) -> bool:
    return (
        isinstance(value, Number) and not isinstance(value, bool) and not pd.isna(value)
    )
