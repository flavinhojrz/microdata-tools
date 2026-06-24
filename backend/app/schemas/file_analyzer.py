from pydantic import BaseModel


class TopValue(BaseModel):
    value: str
    count: int


class ColumnSummary(BaseModel):
    name: str
    dtype: str
    missing_count: int
    missing_percentage: float
    unique_count: int


class NumericSummary(BaseModel):
    name: str
    count: int
    mean: float | None
    min: float | None
    max: float | None
    sum: float | None


class CategoricalSummary(BaseModel):
    name: str
    unique_count: int
    top_values: list[TopValue]


class DateSummary(BaseModel):
    name: str
    min_date: str | None
    max_date: str | None
    valid_dates_count: int


class FileAnalyzerResponse(BaseModel):
    filename: str
    extension: str
    delimiter: str | None
    clean_before_analyze: bool
    rows_count: int
    columns_count: int
    columns: list[str]
    missing_values_count: int
    duplicate_rows_count: int
    empty_columns_count: int
    column_summaries: list[ColumnSummary]
    numeric_summaries: list[NumericSummary]
    categorical_summaries: list[CategoricalSummary]
    date_summaries: list[DateSummary]
