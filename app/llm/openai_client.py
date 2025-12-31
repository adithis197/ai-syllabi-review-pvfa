from openai import OpenAI
import json
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-3.5-turbo"

def call_llm(prompt: str) -> dict:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a compliance audit system. "
                    "Return ONLY valid JSON. "
                    "Do not include markdown, explanations, or extra text."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    raw = response.choices[0].message.content.strip()
    print("Raw LLM response:")
    print(raw)

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        raise RuntimeError(f"LLM returned invalid JSON:\n{raw}")
