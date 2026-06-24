from pydantic import BaseModel


class FileConverterPreviewResponse(BaseModel):
    filename: str
    extension: str
    delimiter: str | None
    target_format: str
    clean_before_convert: bool
    rows_count: int
    columns_count: int
    columns: list[str]
    content_preview: str
