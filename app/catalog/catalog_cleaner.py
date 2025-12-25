import re

def parse_course_block(course_block: str) -> dict:
    """
    Parses a single TAMU catalog course block into title + description.
    Rule:
    - Everything BEFORE 'Credits X' → title
    - Everything FROM 'Credits X' onward → description
    """

    m = re.search(r"(Credits\s+\d+)", course_block, re.IGNORECASE)

    if not m:
        # fallback: no credits found
        return {
            "title": course_block.strip(),
            "description": ""
        }

    title = course_block[:m.start()].strip()
    description = course_block[m.start():].strip()

    return {
        "title": title,
        "description": description
    }
