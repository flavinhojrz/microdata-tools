from typing import Any

from pydantic import BaseModel


class FileCleanerResponse(BaseModel):
    filename: str
    extension: str
    delimiter: str | None
    original_rows_count: int
    original_columns_count: int
    cleaned_rows_count: int
    cleaned_columns_count: int
    removed_empty_rows_count: int
    removed_empty_columns_count: int
    removed_duplicate_rows_count: int
    original_columns: list[str]
    cleaned_columns: list[str]
    preview: list[dict[str, Any]]
