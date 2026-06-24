from pydantic import BaseModel


class FileConverterPreviewResponse(BaseModel):
    filename: str
    extension: str
    delimiter: str | None
    target_format: str
    clean_before_convert: bool
    normalize_brazilian_data: bool
    normalized_numeric_columns: list[str]
    normalized_date_columns: list[str]
    rows_count: int
    columns_count: int
    columns: list[str]
    content_preview: str
