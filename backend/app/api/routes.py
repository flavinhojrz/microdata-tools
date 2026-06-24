from typing import Any

from fastapi import APIRouter, File, UploadFile

from app.schemas.file_preview import FilePreviewResponse
from app.services.file_reader import generate_file_preview

router = APIRouter(prefix="/api")


@router.post("/files/preview", response_model=FilePreviewResponse)
async def preview_file(file: UploadFile = File(...)) -> Any:
    return await generate_file_preview(file)
