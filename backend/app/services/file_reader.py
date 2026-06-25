from csv import Error as CsvError
from csv import Sniffer
from io import BytesIO
from pathlib import Path
from typing import Any

import pandas as pd
from fastapi import HTTPException, UploadFile, status

from app.core.config import get_settings


SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xls"}
CSV_DELIMITERS = [",", ";", "\t", "|"]
CSV_ENCODINGS = ["utf-8-sig", "utf-8", "latin1"]
UPLOAD_CHUNK_SIZE = 64 * 1024


async def generate_file_preview(file: UploadFile) -> dict[str, Any]:
    filename, extension, dataframe, delimiter = await read_uploaded_file(file)

    preview_dataframe = dataframe.head(10)

    return {
        "filename": filename,
        "extension": extension,
        "delimiter": delimiter,
        "rows_count": int(dataframe.shape[0]),
        "columns_count": int(dataframe.shape[1]),
        "columns": [str(column) for column in dataframe.columns],
        "preview": dataframe_to_records(preview_dataframe),
    }


async def read_uploaded_dataframe(file: UploadFile) -> tuple[pd.DataFrame, str | None]:
    _, _, dataframe, delimiter = await read_uploaded_file(file)
    return dataframe, delimiter


async def read_uploaded_file(
    file: UploadFile,
) -> tuple[str, str, pd.DataFrame, str | None]:
    filename = file.filename or ""

    if not filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Arquivo sem nome.",
        )

    extension = Path(filename).suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato não suportado. Envie um arquivo CSV, XLSX ou XLS.",
        )

    settings = get_settings()

    contents = await _read_within_limit(
        file,
        max_bytes=settings.max_upload_size_bytes,
        limit_mb=settings.MAX_UPLOAD_SIZE_MB,
    )

    if not contents:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Arquivo vazio.",
        )

    dataframe, delimiter = _read_dataframe(contents=contents, extension=extension)

    return filename, extension, dataframe, delimiter


async def _read_within_limit(
    file: UploadFile,
    max_bytes: int,
    limit_mb: int,
) -> bytes:
    # Lemos em blocos e abortamos assim que o limite é ultrapassado, sem carregar
    # o arquivo inteiro em memória. Protege o backend de uploads grandes demais.
    chunks: list[bytes] = []
    total = 0

    while True:
        chunk = await file.read(UPLOAD_CHUNK_SIZE)

        if not chunk:
            break

        total += len(chunk)

        if total > max_bytes:
            raise HTTPException(
                status_code=status.HTTP_413_CONTENT_TOO_LARGE,
                detail=(f"Arquivo muito grande. O limite atual é de {limit_mb} MB."),
            )

        chunks.append(chunk)

    return b"".join(chunks)


def _read_dataframe(contents: bytes, extension: str) -> tuple[pd.DataFrame, str | None]:
    try:
        if extension == ".csv":
            dataframe, delimiter = _read_csv(contents)
            return dataframe, delimiter

        dataframe = pd.read_excel(BytesIO(contents))
        return dataframe, None
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não foi possível ler o arquivo. Verifique se ele está válido.",
        ) from error


def _read_csv(contents: bytes) -> tuple[pd.DataFrame, str]:
    sample, encoding = _decode_csv_sample(contents)
    delimiter = _detect_csv_delimiter(sample)

    dataframe = pd.read_csv(
        BytesIO(contents),
        sep=delimiter,
        encoding=encoding,
    )

    return dataframe, delimiter


def _decode_csv_sample(contents: bytes) -> tuple[str, str]:
    sample_bytes = contents[:8192]

    for encoding in CSV_ENCODINGS:
        try:
            return sample_bytes.decode(encoding), encoding
        except UnicodeDecodeError:
            continue

    return sample_bytes.decode("latin1", errors="replace"), "latin1"


def _detect_csv_delimiter(sample: str) -> str:
    try:
        dialect = Sniffer().sniff(sample, delimiters=CSV_DELIMITERS)
        return dialect.delimiter
    except CsvError:
        return _fallback_detect_delimiter(sample)


def _fallback_detect_delimiter(sample: str) -> str:
    lines = [line for line in sample.splitlines() if line.strip()][:5]

    if not lines:
        return ","

    delimiter_scores = {
        delimiter: sum(line.count(delimiter) for line in lines)
        for delimiter in CSV_DELIMITERS
    }

    best_delimiter = max(delimiter_scores, key=delimiter_scores.get)

    if delimiter_scores[best_delimiter] == 0:
        return ","

    return best_delimiter


def dataframe_to_records(dataframe: pd.DataFrame) -> list[dict[str, Any]]:
    clean_dataframe = dataframe.where(pd.notnull(dataframe), None)
    return clean_dataframe.to_dict(orient="records")


def _dataframe_to_records(dataframe: pd.DataFrame) -> list[dict[str, Any]]:
    return dataframe_to_records(dataframe)
