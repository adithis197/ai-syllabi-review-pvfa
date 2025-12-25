import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:7b"
def normalize_details(llm_result: dict) -> dict:
    details = []
    for r in llm_result.get("details", []):
        details.append({
            "id": r.get("id") or r.get("ID"),
            "answer": r.get("answer") or r.get("Answer"),
            "justification": r.get("justification") or r.get("Justification", ""),
            "action_required": (
                r.get("action_required")
                or r.get("Action_Required")
                or None
            )
        })
    return {"details": details}

def call_llm(prompt: str) -> dict:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    raw = response.json().get("response", "").strip()
    print("Raw LLM response:")
    print(raw)

    # Remove ```json wrappers
    if raw.startswith("```"):
        raw = raw.split("```")[1].strip()

    # Remove leading "json"
    if raw.lower().startswith("json"):
        raw = raw[4:].strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        raise RuntimeError(f"LLM returned invalid JSON:\n{raw}")
