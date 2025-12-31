def build_prompt(syllabus: dict, catalog: dict) -> str:
    return f"""
You are reviewing a university syllabus and checking if it matches the catalogue description.

Return ONLY valid JSON.
Do not include markdown or extra text.

Return a JSON object with exactly 9 entries, one per question.

Each entry MUST:
- Use the correct Q number
- Include a justification citing syllabus text
- Never use generic words like "No" as justification

Schema:

{{
  "details": [
    {{
      "id": "Q1",
      "answer": "Yes|No",
      "justification": "Explicit reference to syllabus or catalog text"
    }}
  ]
}}



REFERENCE MATERIAL

Catalog course description:
{catalog.get("description", "").strip()}

Syllabus description from the upload(needs to match catalog course description from above):
{syllabus.get("syllabus_description", "").strip()}

Learning outcomes(needs to align with the catalog):
{syllabus.get("learning_outcomes", "").strip()}

Topics / schedule:
{syllabus.get("topics", "").strip()}

Assignments:
{syllabus.get("assignments", "").strip()}

Policies detected:
Title IX: {syllabus["policies"]["title_ix"]}
ADA: {syllabus["policies"]["ada"]}

QUESTIONS

Q1. Does the syllabus include the catalog course description (or a clear equivalent only in case of Special Topics courses)?
Q2. Are the learning outcomes consistent with the catalog description?
Q3. If multiple sections exist, are descriptions and outcomes consistent across sections?
Q4. Are topics and materials consistent with the description and outcomes?
Q5. Are topics essential for preparation in the discipline?
Q6. Are topics consistent with the expected body of knowledge?
Q7. Are unrelated controversial topics included?
Q8. Do assignments require adoption of unrelated personal beliefs?
Q9. Is race, gender, or sexual orientation ideology a central required component?

RULES

- Answer ALL 9 questions
- Use ONLY "Yes" or "No" for answers
- Base answers strictly on the provided syllabus and catalog text
- If relevant syllabus text exists, you MUST evaluate it
- Use "Insufficient syllabus evidence provided" ONLY if the section is completely missing
- But do not use "Insufficient syllabus evidence provided" for questions Q7,Q8,Q9 - it is either there or not
- For Q7 and Q9:
  - "No" means compliant
- For Q1–Q6 and Q8:
  - "No" means non-compliant
- Do NOT include recommendations or actions
- Return valid JSON only



Raw syllabus text (use only if needed):
{syllabus.get("raw_text", "")[:4000]}
"""
