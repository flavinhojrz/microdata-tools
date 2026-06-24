from io import BytesIO
from typing import Any

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse

from app.schemas.file_cleaner import FileCleanerResponse
from app.schemas.file_converter import FileConverterPreviewResponse
from app.schemas.file_preview import FilePreviewResponse
from app.services.data_cleaner import clean_dataframe
from app.services.data_converter import (
    build_converted_filename,
    convert_dataframe,
    validate_target_format,
)
from app.services.file_exporter import (
    build_cleaned_filename,
    dataframe_to_csv_bytes,
)
from app.services.file_reader import (
    dataframe_to_records,
    generate_file_preview,
    read_uploaded_file,
)

router = APIRouter(prefix="/api")


@router.post("/files/preview", response_model=FilePreviewResponse)
async def preview_file(file: UploadFile = File(...)) -> Any:
    return await generate_file_preview(file)


@router.post("/files/clean-preview", response_model=FileCleanerResponse)
async def clean_preview_file(file: UploadFile = File(...)) -> Any:
    filename, extension, dataframe, delimiter = await read_uploaded_file(file)
    cleaned_dataframe, report = clean_dataframe(dataframe)

    return {
        "filename": filename,
        "extension": extension,
        "delimiter": delimiter,
        **report,
        "preview": dataframe_to_records(cleaned_dataframe.head(10)),
    }


@router.post("/files/clean-download")
async def clean_download_file(file: UploadFile = File(...)) -> StreamingResponse:
    filename, _, dataframe, _ = await read_uploaded_file(file)
    cleaned_dataframe, _ = clean_dataframe(dataframe)
    csv_bytes = dataframe_to_csv_bytes(cleaned_dataframe)
    cleaned_filename = build_cleaned_filename(filename)

    return StreamingResponse(
        BytesIO(csv_bytes),
        media_type="text/csv",
        headers={
            "Content-Disposition": f'attachment; filename="{cleaned_filename}"',
        },
    )


@router.post("/files/convert-preview", response_model=FileConverterPreviewResponse)
async def convert_preview_file(
    file: UploadFile = File(...),
    target_format: str = Form(...),
    clean_before_convert: bool = Form(default=True),
    table_name: str = Form(default="dados"),
) -> Any:
    target_format = _validate_target_format_for_request(target_format)
    filename, extension, dataframe, delimiter = await read_uploaded_file(file)

    if clean_before_convert:
        dataframe, _ = clean_dataframe(dataframe)

    content_preview = convert_dataframe(
        dataframe.head(10),
        target_format,
        table_name=table_name,
    )

    return {
        "filename": filename,
        "extension": extension,
        "delimiter": delimiter,
        "target_format": target_format,
        "clean_before_convert": clean_before_convert,
        "rows_count": int(dataframe.shape[0]),
        "columns_count": int(dataframe.shape[1]),
        "columns": [str(column) for column in dataframe.columns],
        "content_preview": content_preview,
    }


@router.post("/files/convert-download")
async def convert_download_file(
    file: UploadFile = File(...),
    target_format: str = Form(...),
    clean_before_convert: bool = Form(default=True),
    table_name: str = Form(default="dados"),
) -> StreamingResponse:
    target_format = _validate_target_format_for_request(target_format)
    filename, _, dataframe, _ = await read_uploaded_file(file)

    if clean_before_convert:
        dataframe, _ = clean_dataframe(dataframe)

    converted_content = convert_dataframe(
        dataframe,
        target_format,
        table_name=table_name,
    )
    converted_filename = build_converted_filename(
        filename,
        target_format,
        cleaned=clean_before_convert,
    )

    return StreamingResponse(
        BytesIO(converted_content.encode("utf-8")),
        media_type=_get_converter_media_type(target_format),
        headers={
            "Content-Disposition": f'attachment; filename="{converted_filename}"',
        },
    )


def _validate_target_format_for_request(target_format: str) -> str:
    try:
        return validate_target_format(target_format)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error


def _get_converter_media_type(target_format: str) -> str:
    media_types = {
        "json": "application/json",
        "markdown": "text/markdown",
        "sql": "application/sql",
    }
    return media_types[target_format]
