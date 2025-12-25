import json
from app.catalog.catalog_parser import extract_text_from_pdf, split_catalog_by_course
from app.catalog.catalog_cleaner import parse_course_block



UNDERGRAD_PDF = "app/catalog/undergraduate_catalogue.pdf"
GRAD_PDF = "app/catalog/graduate_catalogue.pdf"
OUTPUT_JSON = "app/catalog/catalog.json"


def build_catalog():
    catalog_map = {}

    for pdf_path, level in [
        (UNDERGRAD_PDF, "Undergraduate"),
        (GRAD_PDF, "Graduate")
    ]:
        text = extract_text_from_pdf(pdf_path)
        raw_courses = split_catalog_by_course(text)

        for course_code, block in raw_courses.items():
            parsed = parse_course_block(block)
            parsed["level"] = level
            catalog_map[course_code] = parsed

    with open(OUTPUT_JSON, "w") as f:
        json.dump(catalog_map, f, indent=2)

    print(f"Catalog built with {len(catalog_map)} courses.")


if __name__ == "__main__":
    build_catalog()
