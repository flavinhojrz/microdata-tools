from typing import Any

from pydantic import BaseModel


class FilePreviewResponse(BaseModel):
    filename: str
    extension: str
    delimiter: str | None
    rows_count: int
    columns_count: int
    columns: list[str]
    preview: list[dict[str, Any]]
