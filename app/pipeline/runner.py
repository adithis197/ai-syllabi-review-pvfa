from app.ingestion.parser import parse_syllabus
from app.catalog.loader import load_catalog
from app.pipeline.prompt_builder import build_prompt
from app.llm.openai_client import call_llm
from app.llm.ollama import normalize_details
from app.reports.formatter import format_report
from app.reports.report_builder import build_report
from app.reports.pdf_generator import generate_pdf
from app.pipeline.matrix import BASE_MATRIX

def normalize_q3_for_single_section(report: dict):
    for item in report["details"]:
        if item["id"] == "Q3":
            item["answer"] = "Yes"
            item["justification"] = (
                "The syllabus represents a single course section; "
                "cross-section consistency is not applicable."
            )
            item["action_required"] = None

def run_pipeline(syllabus_pdf_path):
    syllabus = parse_syllabus(syllabus_pdf_path)

    catalog = load_catalog()
    catalog_entry = catalog.get(syllabus["course_code"], {})

    prompt = build_prompt(
        syllabus=syllabus,
        catalog=catalog_entry
    )
    print("Prompt sent to LLM:")
    print(prompt)

    llm_result = call_llm(prompt)   # MUST return dict
    llm_result = normalize_details(llm_result)
    normalize_q3_for_single_section(llm_result)
    attach_actions(llm_result)
    report = format_report(llm_result)

    pdf_path = generate_pdf(report, syllabus["course_code"])

    return {
        "status": "processed",
        "pdf": pdf_path,
        "report": report
    }

from app.pipeline.matrix import BASE_MATRIX

COMPLIANT_NO_QUESTIONS = {"Q7", "Q8", "Q9"}

def attach_actions(report: dict):
    matrix = {q["id"]: q for q in BASE_MATRIX}

    for item in report["details"]:
        qid = item["id"]
        answer = item["answer"]

        # Default
        item["action_required"] = None

        # Non-compliance questions
        if answer == "No" and qid not in COMPLIANT_NO_QUESTIONS:
            item["action_required"] = matrix[qid]["action_if_no"]

        # Compliance-by-No questions (Q7–Q9)
        # No action even if answer is "No"


# from app.ingestion.parser import parse_syllabus
# from app.catalog.loader import load_catalog   # ✅ ADD THIS
# from app.pipeline.prompt_builder import build_prompt
# from app.reports.formatter import format_report
# from app.llm.ollama import call_llm

# def run_pipeline(syllabus_pdf_path):
#     syllabus = parse_syllabus(syllabus_pdf_path)

#     catalog = load_catalog()
#     catalog_entry = catalog.get(syllabus["course_code"], {})

#     prompt = build_prompt(
#         syllabus=syllabus,
#         catalog=catalog_entry
#     )

#     llm_result = call_llm(prompt)
#     print("LLM Result:")
#     print(type(llm_result))
#     print(llm_result)
#     print("End of LLM Result")

#     report = format_report(llm_result)

#     return report
