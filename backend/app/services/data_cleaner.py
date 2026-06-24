import re
import unicodedata
from typing import Any

import pandas as pd


def clean_dataframe(dataframe: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    original_rows_count = int(dataframe.shape[0])
    original_columns_count = int(dataframe.shape[1])
    original_columns = [str(column) for column in dataframe.columns]

    cleaned_dataframe = dataframe.dropna(how="all")
    removed_empty_rows_count = original_rows_count - int(cleaned_dataframe.shape[0])

    cleaned_dataframe = cleaned_dataframe.dropna(axis=1, how="all")
    removed_empty_columns_count = original_columns_count - int(
        cleaned_dataframe.shape[1]
    )

    rows_count_before_deduplication = int(cleaned_dataframe.shape[0])
    cleaned_dataframe = cleaned_dataframe.drop_duplicates()
    removed_duplicate_rows_count = rows_count_before_deduplication - int(
        cleaned_dataframe.shape[0]
    )

    cleaned_dataframe = cleaned_dataframe.copy()
    cleaned_dataframe.columns = normalize_column_names(list(cleaned_dataframe.columns))
    cleaned_columns = [str(column) for column in cleaned_dataframe.columns]

    report = {
        "original_rows_count": original_rows_count,
        "original_columns_count": original_columns_count,
        "cleaned_rows_count": int(cleaned_dataframe.shape[0]),
        "cleaned_columns_count": int(cleaned_dataframe.shape[1]),
        "removed_empty_rows_count": removed_empty_rows_count,
        "removed_empty_columns_count": removed_empty_columns_count,
        "removed_duplicate_rows_count": removed_duplicate_rows_count,
        "original_columns": original_columns,
        "cleaned_columns": cleaned_columns,
    }

    return cleaned_dataframe, report


def normalize_column_name(column: object) -> str:
    if _is_missing_column_name(column):
        return "coluna"

    text = str(column).strip().lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(character for character in text if not _is_accent(character))
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")

    return text or "coluna"


def normalize_column_names(columns: list[object]) -> list[str]:
    normalized_columns: list[str] = []
    base_counts: dict[str, int] = {}
    used_columns: set[str] = set()

    for column in columns:
        base_name = normalize_column_name(column)
        count = base_counts.get(base_name, 0)
        candidate = base_name if count == 0 else f"{base_name}_{count + 1}"

        while candidate in used_columns:
            count += 1
            candidate = f"{base_name}_{count + 1}"

        base_counts[base_name] = count + 1
        used_columns.add(candidate)
        normalized_columns.append(candidate)

    return normalized_columns


def _is_missing_column_name(column: object) -> bool:
    if column is None:
        return True

    try:
        return bool(pd.isna(column))
    except (TypeError, ValueError):
        return False


def _is_accent(character: str) -> bool:
    return unicodedata.category(character) == "Mn"
