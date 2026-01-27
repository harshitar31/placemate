import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.1:8b"

SYSTEM_PROMPT = """
You are a placement data analyst.

Rules:
- Explain historical patterns only.
- Anchor explanations to the exact CGPA threshold provided.
- Do NOT replace the threshold with a lower or different value.
- Do NOT assess eligibility.
- Do NOT give advice or predictions.
- Do NOT use second-person language.
- Base explanations strictly on provided data.
- Use phrases like "based on historical data" and "covers X% of roles".

"""

def generate_answer(analysis_output, question: str) -> str:
    prompt = f"""
Historical data:
{analysis_output}

Question:
{question}

Explain the observed pattern clearly and concisely.
"""

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "stream": False,
        "temperature": 0.2
    }

    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()

    return response.json()["message"]["content"].strip()
