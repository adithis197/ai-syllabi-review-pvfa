# PVFA AI Syllabus Review App 

## 1. Project Purpose

The app allows a user to upload a course syllabus PDF and generates a PVFA syllabus review report. The report checks the uploaded syllabus against a syllabus review matrix and compares extracted syllabus content with TAMU catalog/course description information.

The current app is intended for internal review/support, not as a final authoritative compliance decision. Human review is still required.

## 2. High-Level Workflow

```text
User uploads syllabus PDF
        ↓
FastAPI upload route saves PDF temporarily
        ↓
pypdf extracts raw text from the PDF
        ↓
Regex-based parser extracts course code, description, outcomes, topics, assignments, and policy flags
        ↓
Catalog data is loaded from local catalog.json/LLM response
        ↓
Prompt is built using syllabus text + catalog context + review matrix questions
        ↓
OpenAI GPT API evaluates the syllabus and returns JSON
        ↓
The JSON result is normalized and formatted
        ↓
ReportLab generates a final PDF report
        ↓
PDF report is saved in the output/ folder and shown on the dashboard
```

## 3. Main Technologies Used

- **Backend framework:** FastAPI
- **Server/runtime:** Uvicorn
- **Template rendering:** Jinja2
- **PDF text extraction:** pypdf
- **PDF report generation:** ReportLab
- **LLM provider:** OpenAI API
- **Current OpenAI model in code:** `gpt-3.5-turbo`
- **OpenAI SDK version in requirements:** `openai==2.14.0`
- **Python runtime:** Python 3.11.9
- **Deployment:** Render
- **Storage currently used by live app:** local folder / persistent filesystem behavior, not a formal database


## 4. Important Files and Folders

```text
app/main.py
```
Main FastAPI application. Handles routes such as `/`, `/upload`, and `/dashboard`. Uploaded files are saved into `temp/`, processed through the pipeline, and the dashboard lists reports from `output/`.

```text
app/ingestion/parser.py
```
Extracts text from uploaded PDFs using `pypdf`. It uses best-effort regex matching to identify:

- course code
- course description
- learning outcomes
- topics / schedule
- assignments / grading
- policy flags such as Title IX and ADA
- raw syllabus text

```text
app/catalog/catalog.json
```
Local catalog data used for course lookup.

```text
app/catalog/undergraduate_catalogue.pdf
app/catalog/graduate_catalogue.pdf
```
Catalog PDFs included in the repo.

```text
app/pipeline/prompt_builder.py
```
Builds the full LLM prompt. This is where most syllabus review logic currently lives, including the 9 review questions and compliance interpretation rules.

```text
app/llm/openai_client.py
```
Calls the OpenAI Chat Completions API using:

```python
MODEL = "gpt-3.5-turbo"
```

The request uses `temperature=0` and expects the model to return valid JSON only.

```text
app/pipeline/runner.py
```
Coordinates the full pipeline:

1. parse syllabus
2. load catalog
3. build prompt
4. call OpenAI
5. normalize output
6. attach action items
7. format report
8. generate PDF


## 5. Environment Variables

The live app needs:

```bash
OPENAI_API_KEY=<OpenAI API key>
```

## 6. How to Run Locally

```bash
git clone https://github.com/adithis197/ai-syllabi-review-pvfa.git
cd ai-syllabi-review-pvfa
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file:

```bash
OPENAI_API_KEY=your_key_here
```

Run the app:

```bash
uvicorn app.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000
```