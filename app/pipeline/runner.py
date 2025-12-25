from app.ingestion.parser import parse_syllabus
from app.catalog.loader import load_catalog
from app.pipeline.prompt_builder import build_prompt
from app.llm.ollama import call_llm, normalize_details
from app.reports.formatter import format_report
from app.reports.report_builder import build_report
from app.reports.pdf_generator import generate_pdf

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
    report = format_report(llm_result)

    pdf_path = generate_pdf(report, syllabus["course_code"])

    return {
        "status": "processed",
        "pdf": pdf_path,
        "report": report
    }


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
