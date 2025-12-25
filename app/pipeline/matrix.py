BASE_MATRIX = [
    {
        "id": "Q1",
        "scope": "single",
        "question": "Does the syllabus include the current catalog course description?",
        "action_if_no": "Instructor must change the syllabus to match the current catalog course description."
    },
    {
        "id": "Q2",
        "scope": "single",
        "question": "Are the learning outcomes consistent with the course description in the current catalog?",
        "action_if_no": "Instructor should adjust learning outcomes to match the course description."
    },
    {
        "id": "Q3",
        "scope": "multi",
        "question": "If a multi-section course, are the course description and learning outcomes consistent across all sections?",
        "action_if_no": "Instructor(s) must change the syllabus to match the catalog description and ensure consistency across sections."
    },
    {
        "id": "Q4",
        "scope": "single",
        "question": "Are course materials and topics consistent with the course description and learning outcomes?",
        "action_if_no": "Instructor must adjust materials to be consistent with approved course information."
    },
    {
        "id": "Q5",
        "scope": "single",
        "question": "Are topics covered essential for students to be prepared to enter their profession or discipline?",
        "action_if_no": "Faculty and department leadership should justify educational value or adjust course content."
    },
    {
        "id": "Q6",
        "scope": "single",
        "question": "Are topics covered consistent with the expected body of knowledge in the discipline?",
        "action_if_no": "Faculty and department leadership should adjust topics for future offerings."
    },
    {
        "id": "Q7",
        "scope": "single",
        "question": "Are controversial topics presented that have no relation to the approved course description and learning outcomes?",
        "action_if_no": "Instructor should revise content to align with approved course description and outcomes."
    },
    {
        "id": "Q8",
        "scope": "single",
        "question": "Do any assignments require students to hold certain beliefs unrelated to the approved course description and outcomes to receive a grade?",
        "action_if_no": "Instructor should revise assignments to align with approved course description and outcomes."
    },
    {
        "id": "Q9",
        "scope": "single",
        "question": "Does the course content include material related to race ideology, gender ideology, or sexual orientation?",
        "action_if_no": "Department head should ensure alternative options exist and conduct additional review."
    }
]



def evaluate_matrix(syllabus_data, llm_call):
    results = []

    for q in BASE_MATRIX:
        prompt = f"""
        Syllabus:
        {syllabus_data}

        Question:
        {q['question']}

        Answer Yes or No with justification.
        """

        answer = llm_call(prompt)

        result = {
            "id": q["id"],
            "question": q["question"],
            "answer": answer,
            "action_required": (
                q["action_if_no"] if "No" in answer else None
            )
        }
        results.append(result)

    return results
