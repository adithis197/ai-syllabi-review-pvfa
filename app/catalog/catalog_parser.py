import re
from pypdf import PdfReader


COURSE_CODE_REGEX = r"\b[A-Z]{3,4}\s\d{3}\b"

def normalize_text(text: str) -> str:
    if not text:
        return ""

    text = text.replace("\u00a0", " ")

    # Insert space before 'Credits' if missing
    text = re.sub(r'(?<!\s)(Credits)', r' \1', text)

    # Split merged lowercase-uppercase words (best effort)
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)

    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


def extract_text_from_pdf(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def split_catalog_by_course(text: str) -> dict:
    matches = list(re.finditer(COURSE_CODE_REGEX, text))
    catalog = {}

    i = 0
    while i < len(matches):
        match = matches[i]
        course_code = match.group().replace("\u00a0", " ").strip()
        start = match.start()

        # Step 1: find the first occurrence of "Credits <number>" AFTER this course code
        credits_match = re.search(
            r"Credits\s+\d+",
            text[match.end():],
            re.IGNORECASE
        )

        if credits_match:
            credits_end = match.end() + credits_match.end()
        else:
            # fallback: behave like old logic
            credits_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)

        # Step 2: find next course code AFTER credits
        next_match_index = i + 1
        while next_match_index < len(matches) and matches[next_match_index].start() < credits_end:
            next_match_index += 1

        end = (
            matches[next_match_index].start()
            if next_match_index < len(matches)
            else len(text)
        )

        block = normalize_text(text[start:end])
        catalog[course_code] = block

        # Step 3: handle immediate cross-listed code (e.g., VIZA 654/CSCE 646)
        if (
            i + 1 < len(matches)
            and text[match.end():matches[i + 1].start()].strip().startswith("/")
        ):
            cross_code = matches[i + 1].group().replace("\u00a0", " ").strip()
            catalog[cross_code] = block
            i += 2
        else:
            i += 1

    return catalog

