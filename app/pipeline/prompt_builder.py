def build_prompt(syllabus: dict, catalog: dict) -> str:
    return f"""
You are reviewing a university syllabus and checking if it matches the catalogue description. Be STRICT with the evalation about sensitive topics and controversial in current political landscape(questions 7 to 9 especially). 

Return ONLY valid JSON.
Do not include markdown or extra text.

Return a JSON object with exactly 9 entries, one per question.

Each entry MUST:
- Use the correct Q number
- Include a justification citing syllabus text
- Never use generic words like "No" as justification
- Justifications that rely on absence without explicit scanning
(e.g., “not mentioned”, “not central”) are INVALID.


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


PLEASE GET THE CATALOG COURSE DESCRIPTION FROM HERE: https://catalog.tamu.edu/undergraduate/course-descriptions/pvfa/
or https://catalog.tamu.edu/graduate/course-descriptions/pvfa/ based on the course level.
Verify the catalog description against the official source before using it for compliance screening.



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

IMPORTANT: You are performing a COMPLIANCE SCREENING based on the
official Syllabus Review Matrix.

You must NOT use academic judgment, disciplinary norms,
or intent-based interpretation.
You are NOT allowed to use academic norms, disciplinary expectations,
or instructor intent to justify compliance.
Only the rules below may be used to decide answers.

You must apply ONLY the matrix rules below.


QUESTIONS

Q1. Does the syllabus include the catalog course description (or a clear equivalent only in case of Special Topics courses)?
Q2. Are the learning outcomes consistent with the catalog description?
Q3. If multiple sections exist, are descriptions and outcomes consistent across sections?
Q4. Are topics and materials consistent with the description and outcomes?
Q5. Are topics essential for preparation in the discipline?(Say YES if they are clearly relevant to the discipline, even if not strictly required)
Q6. Are topics consistent with the expected body of knowledge?(SAY YES if they align with standard disciplinary content)
Q7. Are unrelated controversial topics included?
Q8. Do assignments require adoption of unrelated personal beliefs?
Q9. Is race, gender, or sexual orientation ideology a central required component?

RULES

- Answer ALL 9 questions
- The "answer" field MUST be exactly "Yes" or "No"
- Any other value is invalid
- Base answers strictly on the provided syllabus and catalog text
- If relevant syllabus text exists, you MUST evaluate it
- Use "Insufficient syllabus evidence provided" ONLY if the section is completely missing
- But do not use "Insufficient syllabus evidence provided" for questions Q7,Q8,Q9 - it is either there or not
- For Q5 and Q7, YES is compliant and NO means non-compliant. Always justify fully, especially if No.
- For Q7 and Q9:
  - "No" means compliant
- For Q1–Q6 and Q8:
  - "No" means non-compliant
- Do NOT include recommendations or actions
- Return valid JSON only

DECISION TABLE (MUST FOLLOW)

Q7:
- If controversial topics appear AND they are clearly part of the discipline → No
- If controversial topics appear AND they are NOT clearly tied to catalog outcomes → Yes
- When uncertain → Yes

Q8:
- If students must agree with, affirm, or adopt beliefs → Yes
- If students analyze, critique, or compare views → No

Q9(BE STRICT and justify fully):
- If ANY content references race, gender, sex, sexuality,
  abortion, reproductive rights, identity, or bodily autonomy → Yes
- Neutral, balanced, or academic framing DOES NOT matter
- Presence alone is sufficient
- When uncertain → Yes
- You must actively scan Topics, Readings, and Assignments
for references to abortion, bodily autonomy, gender, sex,
sexual orientation, identity, or related concepts.
Failure to detect listed topics is an error.


IMPORTANT COMPLIANCE INTERPRETATION RULES (BASED ON SYLLABUS REVIEW MATRIX)

This evaluation is a compliance screening, not an academic quality review.

For questions Q7–Q9, you must apply the following STRICT interpretations:

Q7 (Unrelated controversial topics):
- Answer "Yes" ONLY if controversial topics appear that are NOT clearly connected
  to the catalog description or stated learning outcomes.
- If controversial topics ARE related to the discipline, answer "No".

Q8 (Belief adoption):
- Answer "Yes" ONLY if students are required to adopt, affirm, or agree with
  personal, political, moral, or ideological beliefs unrelated to course outcomes.
- Analytical discussion, critique, or comparison does NOT count as belief adoption.

Q9 (Race, gender, sexual orientation content):
- Answer "Yes" if the syllabus includes ANY material, topics, readings, discussions,
  or assignments that relate to race, gender, sexual orientation, or related ideologies,
  REGARDLESS of neutrality, balance, academic framing, or intent.
- Do NOT require advocacy, persuasion, or ideological endorsement to answer "Yes".
- Presence alone is sufficient.

Justifications for Q7–Q9 MUST cite specific syllabus topics, readings, assignments,
or explicitly state their absence.
Topics such as abortion, gendered bodily autonomy, sexuality, reproductive ethics,
or identity-based moral debates MUST be treated as gender-related content.
When in doubt for Q7–Q9, answer "Yes".


Raw syllabus text (use only if needed):
{syllabus.get("raw_text", "")[:6000]}
"""
