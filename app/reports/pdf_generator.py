from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from app.pipeline.matrix import BASE_MATRIX

QUESTION_MAP = {q["id"]: q for q in BASE_MATRIX}


def draw_wrapped_block(c, text, x, y, max_chars, leading, height):
    """
    Draw wrapped text and auto-handle page breaks.
    Returns updated y position.
    """
    lines = wrap_text(text, max_chars)

    for line in lines:
        if y < 80:
            c.showPage()
            c.setFont("Helvetica", 10)
            y = height - 50
        c.drawString(x, y, line)
        y -= leading

    return y


def generate_pdf(report: dict, course_code: str) -> str:
    output_path = f"output/{course_code}_PVFA_Report.pdf"

    c = canvas.Canvas(output_path, pagesize=LETTER)
    width, height = LETTER

    y = height - 50

    # ---------- Title ----------
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "PVFA Syllabus Review Report")
    y -= 20

    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Course: {course_code}")
    y -= 30

    # ---------- Main Questions ----------
    for item in report["details"]:
        q = QUESTION_MAP[item["id"]]

        if y < 120:
            c.showPage()
            y = height - 50

        # Question (wrapped)
        c.setFont("Helvetica-Bold", 11)
        y = draw_wrapped_block(
            c,
            f"{item['id']}. {q['question']}",
            x=50,
            y=y,
            max_chars=90,
            leading=14,
            height=height
        )

        y -= 5

        # Answer (bold)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(70, y, item["answer"].upper())
        y -= 14

        # Justification (wrapped)
        if item.get("justification"):
            c.setFont("Helvetica", 10)
            y = draw_wrapped_block(
                c,
                item["justification"],
                x=70,
                y=y,
                max_chars=95,
                leading=12,
                height=height
            )

        y -= 12

    # ---------- Action Required Section ----------
    actions = [
    (item["id"], item["action_required"])
    for item in report["details"]
    if item.get("action_required")
]


    if actions:
        if y < 120:
            c.showPage()
            y = height - 50

        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "Action Required")
        y -= 20

        c.setFont("Helvetica", 11)
        for qid, action in actions:
            y = draw_wrapped_block(
                c,
                f"{qid}: {action}",
                x=50,
                y=y,
                max_chars=95,
                leading=14,
                height=height
            )
            y -= 8

    c.save()
    return output_path


def wrap_text(text, max_chars):
    """Simple text wrapper"""
    words = text.split()
    lines = []
    current = ""

    for word in words:
        if len(current) + len(word) + 1 <= max_chars:
            current += " " + word
        else:
            lines.append(current.strip())
            current = word

    if current:
        lines.append(current.strip())

    return lines
