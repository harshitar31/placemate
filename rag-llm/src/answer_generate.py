import json
from config import OLLAMA_URL, MODEL_NAME

MODEL = MODEL_NAME

SYSTEM_PROMPT = """
You are a placement information assistant.

Rules:
- Answer using ONLY the provided context.
- Look both at the question and context
- State facts and comparisons; do NOT answer using yes/no decisions.
- You may compare a given CGPA value against stated minimum CGPA requirements.
- Do NOT predict placement outcomes.
- Do NOT assess or guarantee eligibility.
- If information is missing, say so clearly.
- Be neutral, factual, and concise.


"""

import httpx

async def generate_answer(analysis_output, question: str, stream: bool = False, chat_history: list = None):
    """
    Generate answer from context asynchronously.
    
    Args:
        analysis_output: Context to use for answering
        question: User's question
        stream: If True, yields answer chunks as they arrive. If False, returns complete answer.
        chat_history: Optional list of previous question/answer dictionaries
    
    Returns:
        If stream=False: Complete answer string
        If stream=True: Async generator yielding answer chunks
    """
    
    # Build prompt with history
    history_context = ""
    if chat_history:
        history_context = "Previous Conversation:\n"
        for msg in chat_history:
            role = "User" if msg["role"] == "user" else "Assistant"
            history_context += f"{role}: {msg['content']}\n"
        history_context += "\n"

    prompt = f"""
{history_context}Context:
{analysis_output}

Question:
{question}

Answer the question using ONLY the context above.
"""

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "stream": stream,
        "temperature": 0.2
    }

    if stream:
        return _generate_streaming(payload)
    else:
        return await _generate_complete(payload)


async def _generate_complete(payload):
    """Generate complete answer asynchronously without streaming."""
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        return response.json()["message"]["content"].strip()


async def _generate_streaming(payload):
    """Generate answer asynchronously with streaming."""
    async with httpx.AsyncClient(timeout=60.0) as client:
        async with client.stream("POST", OLLAMA_URL, json=payload) as response:
            response.raise_for_status()
            
            async for line in response.aiter_lines():
                if line:
                    try:
                        chunk = json.loads(line)
                        if "message" in chunk and "content" in chunk["message"]:
                            content = chunk["message"]["content"]
                            if content:
                                yield content
                    except json.JSONDecodeError:
                        continue

