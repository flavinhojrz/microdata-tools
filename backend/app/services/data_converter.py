import json
from datetime import date, datetime, time
from numbers import Number
from pathlib import Path
from typing import Any

import pandas as pd

from app.services.data_cleaner import normalize_column_name


SUPPORTED_TARGET_FORMATS = {"json", "markdown", "sql"}
FORMAT_EXTENSIONS = {
    "json": "json",
    "markdown": "md",
    "sql": "sql",
}
DEFAULT_CONVERTED_FILENAME_STEM = "dados"


def validate_target_format(target_format: str) -> str:
    normalized_format = target_format.strip().lower()

    if normalized_format not in SUPPORTED_TARGET_FORMATS:
        supported_formats = ", ".join(sorted(SUPPORTED_TARGET_FORMATS))
        raise ValueError(
            f"Formato de destino inválido. Use um destes formatos: {supported_formats}."
        )

    return normalized_format


def dataframe_to_json_string(dataframe: pd.DataFrame) -> str:
    records = _dataframe_to_records(dataframe)
    return json.dumps(records, ensure_ascii=False, indent=2, default=str)


def dataframe_to_markdown_string(dataframe: pd.DataFrame) -> str:
    columns = [_escape_markdown_value(str(column)) for column in dataframe.columns]

    if not columns:
        return ""

    lines = [
        f"| {' | '.join(columns)} |",
        f"| {' | '.join(['---'] * len(columns))} |",
    ]

    for _, row in dataframe.iterrows():
        values = [
            _escape_markdown_value(_format_markdown_value(row.iloc[index]))
            for index in range(len(columns))
        ]
        lines.append(f"| {' | '.join(values)} |")

    return "\n".join(lines)


def dataframe_to_sql_insert_string(
    dataframe: pd.DataFrame,
    table_name: str = "dados",
) -> str:
    sql_table_name = _sanitize_sql_table_name(table_name)
    sql_columns = _sanitize_sql_column_names(list(dataframe.columns))

    if not sql_columns:
        return ""

    columns_sql = ", ".join(sql_columns)
    insert_statements: list[str] = []

    for _, row in dataframe.iterrows():
        values_sql = ", ".join(
            _format_sql_value(row.iloc[index]) for index in range(len(sql_columns))
        )
        insert_statements.append(
            f"INSERT INTO {sql_table_name} ({columns_sql}) VALUES ({values_sql});"
        )

    return "\n".join(insert_statements)


def build_converted_filename(
    original_filename: str,
    target_format: str,
    cleaned: bool = True,
) -> str:
    normalized_format = validate_target_format(target_format)
    extension = FORMAT_EXTENSIONS[normalized_format]

    stem = Path(original_filename).stem.strip() if original_filename else ""

    if not stem or not stem.strip("."):
        stem = DEFAULT_CONVERTED_FILENAME_STEM

    suffix = "_clean" if cleaned else ""
    return f"{stem}{suffix}.{extension}"


def convert_dataframe(
    dataframe: pd.DataFrame,
    target_format: str,
    table_name: str = "dados",
) -> str:
    normalized_format = validate_target_format(target_format)

    if normalized_format == "json":
        return dataframe_to_json_string(dataframe)

    if normalized_format == "markdown":
        return dataframe_to_markdown_string(dataframe)

    return dataframe_to_sql_insert_string(dataframe, table_name=table_name)


def _dataframe_to_records(dataframe: pd.DataFrame) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    columns = [str(column) for column in dataframe.columns]

    for _, row in dataframe.iterrows():
        record = {
            column: _to_python_value(row.iloc[index])
            for index, column in enumerate(columns)
        }
        records.append(record)

    return records


def _to_python_value(value: Any) -> Any:
    if _is_missing_value(value):
        return None

    if isinstance(value, pd.Timestamp):
        return value.isoformat()

    if isinstance(value, datetime | date | time):
        return value.isoformat()

    if hasattr(value, "item"):
        try:
            return value.item()
        except (AttributeError, ValueError):
            return value

    return value


def _format_markdown_value(value: Any) -> str:
    python_value = _to_python_value(value)

    if python_value is None:
        return ""

    return str(python_value).replace("\n", "<br>")


def _escape_markdown_value(value: str) -> str:
    return value.replace("|", r"\|")


def _format_sql_value(value: Any) -> str:
    python_value = _to_python_value(value)

    if python_value is None:
        return "NULL"

    if isinstance(python_value, bool):
        return "TRUE" if python_value else "FALSE"

    if isinstance(python_value, Number):
        return str(python_value)

    escaped_value = str(python_value).replace("'", "''")
    return f"'{escaped_value}'"


def _sanitize_sql_table_name(table_name: str) -> str:
    table_name = table_name.strip() if table_name else ""

    if not table_name:
        return DEFAULT_CONVERTED_FILENAME_STEM

    return _ensure_valid_sql_identifier(
        normalize_column_name(table_name),
        fallback=DEFAULT_CONVERTED_FILENAME_STEM,
    )


def _sanitize_sql_column_names(columns: list[object]) -> list[str]:
    sanitized_columns: list[str] = []
    base_counts: dict[str, int] = {}
    used_columns: set[str] = set()

    for column in columns:
        base_name = _ensure_valid_sql_identifier(
            normalize_column_name(column),
            fallback="coluna",
        )
        count = base_counts.get(base_name, 0)
        candidate = base_name if count == 0 else f"{base_name}_{count + 1}"

        while candidate in used_columns:
            count += 1
            candidate = f"{base_name}_{count + 1}"

        base_counts[base_name] = count + 1
        used_columns.add(candidate)
        sanitized_columns.append(candidate)

    return sanitized_columns


def _ensure_valid_sql_identifier(identifier: str, fallback: str) -> str:
    if not identifier:
        return fallback

    if identifier[0].isdigit():
        return f"{fallback}_{identifier}"

    return identifier


def _is_missing_value(value: Any) -> bool:
    try:
        return bool(pd.isna(value))
    except (TypeError, ValueError):
        return False
