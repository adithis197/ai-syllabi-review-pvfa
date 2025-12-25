import os
from fastapi import APIRouter

router = APIRouter()

OUTPUT_DIR = "output"

@router.get("/api/reports")
def list_reports():
    files = [
        f for f in os.listdir(OUTPUT_DIR)
        if f.endswith(".pdf")
    ]

    return {
        "reports": [
            {
                "filename": f,
                "url": f"/reports/{f}"
            }
            for f in sorted(files)
        ]
    }
