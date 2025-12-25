# app/reports/builder.py

from app.pipeline.matrix import BASE_MATRIX

def build_report(llm_result: dict) -> dict:
    """
    Combines LLM answers with deterministic actions from BASE_MATRIX
    """
    llm_map = {d["id"]: d for d in llm_result["details"]}

    details = []
    issues = 0

    for q in BASE_MATRIX:
        qid = q["id"]
        llm_entry = llm_map.get(qid)

        answer = llm_entry["answer"]
        justification = llm_entry["justification"]

        action_required = None
        if answer == "No":
            action_required = q["action_if_no"]
            issues += 1

        details.append({
            "id": qid,
            "question": q["question"],
            "answer": answer,
            "justification": justification,
            "action_required": action_required
        })

    return {
        "summary": {
            "total": len(BASE_MATRIX),
            "issues": issues
        },
        "details": details
    }
