from io import BytesIO
from pathlib import Path
from typing import Any

import pandas as pd
from fastapi import HTTPException, UploadFile, status


SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xls"}


async def generate_file_preview(file: UploadFile) -> dict[str, Any]:
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

    contents = await file.read()

    if not contents:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Arquivo vazio.",
        )

    dataframe = _read_dataframe(contents=contents, extension=extension)

    preview_dataframe = dataframe.head(10)

    return {
        "filename": filename,
        "extension": extension,
        "rows_count": int(dataframe.shape[0]),
        "columns_count": int(dataframe.shape[1]),
        "columns": [str(column) for column in dataframe.columns],
        "preview": _dataframe_to_records(preview_dataframe),
    }


def _read_dataframe(contents: bytes, extension: str) -> pd.DataFrame:
    buffer = BytesIO(contents)

    try:
        if extension == ".csv":
            return pd.read_csv(buffer)

        return pd.read_excel(buffer)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não foi possível ler o arquivo. Verifique se ele está válido.",
        ) from error


def _dataframe_to_records(dataframe: pd.DataFrame) -> list[dict[str, Any]]:
    clean_dataframe = dataframe.where(pd.notnull(dataframe), None)
    return clean_dataframe.to_dict(orient="records")
