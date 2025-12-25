from fastapi import APIRouter, UploadFile, File
from fastapi.responses import RedirectResponse
from pathlib import Path
import os

from app.pipeline.runner import run_pipeline

router = APIRouter()

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_syllabus(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Run pipeline
    result = run_pipeline(file_path)

    # Extract PDF path safely
    pdf_path = result["pdf_path"]
    filename = os.path.basename(pdf_path)

    # Redirect to dashboard with PDF
    return RedirectResponse(
        url=f"/dashboard?file={filename}",
        status_code=303
    )
