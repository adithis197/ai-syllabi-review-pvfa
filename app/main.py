from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import os
import shutil

from app.pipeline.runner import run_pipeline


app = FastAPI()

app.mount("/reports", StaticFiles(directory="output"), name="reports")
templates = Jinja2Templates(directory="templates")


@app.get("/")
def root():
    return RedirectResponse("/dashboard")


@app.get("/upload")
def upload_page(request: Request):
    return templates.TemplateResponse(
        "upload.html",
        {"request": request}
    )


@app.post("/upload")
async def upload_syllabus(file: UploadFile = File(...)):
    temp_path = f"temp/{file.filename}"
    os.makedirs("temp", exist_ok=True)

    with open(temp_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    result = run_pipeline(temp_path)
    pdf_path = result["pdf"]
    filename = os.path.basename(pdf_path)

    return RedirectResponse(
        url=f"/dashboard?open={filename}",
        status_code=303
    )


@app.get("/dashboard")
def dashboard(request: Request, open: str | None = None):
    reports = sorted(
        os.listdir("output"),
        reverse=True
    )

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "reports": reports,
            "latest_report": reports[0] if reports else None,
            "active_tab": "dashboard"
        }
    )