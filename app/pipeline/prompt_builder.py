def build_prompt(syllabus: dict, catalog: dict) -> str:
    return f"""
You are reviewing a university syllabus and checking if it matches the catalogue description.

Return ONLY valid JSON.
Do not include markdown or extra text.

Return exactly this structure:

{{
  "details": [
    {{
      "id": "Q1",
      "answer": "Yes|No",
      "justification": "string",
      "action_required": null|string
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

- Answer all 9 questions
- Use Yes or No only
- If evidence is missing, answer No and say "Insufficient syllabus evidence provided" and if sensitive content like Q7 and Q9 are not present, answer No with justification "No such content detected"
- Provide action_required ONLY when the answer indicates a compliance issue
- For questions asking whether the syllabus includes prohibited or unrelated content,
  an answer of "No" means compliant and requires no action
- For Q6, check if the topics align with standard discipline knowledge
- Base answers only on provided text

Raw syllabus text (use only if needed):
{syllabus.get("raw_text", "")[:4000]}
"""
