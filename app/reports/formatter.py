def format_report(llm_result: dict) -> dict:
    details = llm_result.get("details", [])

    return {
        "summary": {
            "total": 9,
            "issues": sum(
                1 for r in details
                if r.get("action_required")
            )
        },
        "details": details
    }

