import requests
import json
import re

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.1:8b"

SYSTEM_PROMPT = """
You are an intent classifier for a placement analytics system.

This system answers historical questions about placement data.

Supported intents:
- cgpa_trend            (how CGPA requirements changed)
- cgpa_coverage         (whether a CGPA value meets most historical cutoffs)
- package_trend
- role_history
- company_overview
- placement_statistics
- policy_explanation

Rules:
- If the question asks whether a specific CGPA is "enough", "safe", or "sufficient",
  classify it as cgpa_coverage.
- Extract the CGPA value as cgpa_threshold if mentioned.
- Do NOT assess eligibility.
- Do NOT give advice.
- If CGPA is not mentioned, set cgpa_threshold to null.

Extract if mentioned:
- company name
- CGPA numeric value

Output ONLY valid JSON.

JSON format:
{
  "intent": string,
  "company": string or null,
  "cgpa_threshold": number or null
}

"""

def extract_intent(query: str) -> dict:
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ],
        "stream": False,
        "temperature": 0
    }

    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()

    content = response.json()["message"]["content"]

    match = re.search(r"\{.*\}", content, re.DOTALL)
    if not match:
        raise ValueError(f"Invalid intent output:\n{content}")

    return json.loads(match.group(0))
