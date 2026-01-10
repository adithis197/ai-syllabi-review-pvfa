import re
from pypdf import PdfReader

COURSE_HEADER_REGEX = re.compile(
    r"""
    (?P<codes>[A-Z]{3,4}\s\d{3}(?:\s*/\s*[A-Z]{3,4}\s\d{3})*)   # VIZA 656 / CSCE 647
    \s+
    (?P<title>.+?)                                           # Course title
    \s+
    Credits\s+(?P<credits>\d+)                               # Credits
    """,
    re.VERBOSE
)


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
    catalog = {}
    text = normalize_text(text)

    matches = list(COURSE_HEADER_REGEX.finditer(text))

    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)

        block = text[start:end].strip()

        codes = match.group("codes")
        title = match.group("title").strip()

        for code in codes.split("/"):
            code = code.strip()
            catalog[code] = {
                "title": title,
                "description": block,
                "level": "Graduate"
            }

    return catalog

