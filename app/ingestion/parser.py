from pypdf import PdfReader
import re

def extract_text_from_pdf(path: str) -> str:
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def parse_syllabus(pdf_path: str) -> dict:
    text = extract_text_from_pdf(pdf_path)

    def loose_extract(headers, max_len=2000):
        """
        Best-effort extraction.
        Grabs text after header without assuming formatting.
        """
        for h in headers:
            m = re.search(
                rf"{h}(.{{0,{max_len}}})",
                text,
                re.I | re.S
            )
            if m:
                return m.group(1).strip()
        return ""

    course_code_match = re.search(r"\b[A-Z]{3,4}\s\d{3}\b", text)

    return {
        "course_code": course_code_match.group(0) if course_code_match else None,

        # ⬇️ THESE WERE EMPTY BEFORE
        "syllabus_description": loose_extract(
            ["Course Description", "Description"]
        ),

        "learning_outcomes": loose_extract(
            ["Learning Outcomes", "Course Objectives", "Student Learning Outcomes"]
        ),

        "topics": loose_extract(
            ["Course Topics", "Schedule", "Weekly Schedule", "Course Schedule"]
        ),

        "assignments": loose_extract(
            ["Assignments", "Grading", "Evaluation", "Assessment"]
        ),

        "policies": {
            "title_ix": bool(re.search(r"Title\s*IX", text, re.I)),
            "ada": bool(re.search(r"ADA|Disabilit", text, re.I)),
        },

        # 🔑 ALWAYS INCLUDE RAW TEXT (CRITICAL)
        "raw_text": text
    }
