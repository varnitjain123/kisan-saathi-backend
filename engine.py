import json
import re
from groq import Groq
from prompt import SYSTEM_PROMPT

_client = None

def _get_client():
    global _client
    if _client is None:
        from dotenv import load_dotenv
        import os
        load_dotenv()
        _client = Groq(api_key=os.environ["GROQ_API_KEY"])
    return _client

def _parse_response(raw: str) -> dict:
    cleaned = re.sub(r"```(?:json)?|```", "", raw).strip()
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        return {
            "status": "asking",
            "question": cleaned or "क्या आप अपनी समस्या फिर से बता सकते हैं?",
            "diagnosis": None,
            "advice": None,
        }
    return {
        "status": data.get("status", "asking"),
        "question": data.get("question") or None,
        "diagnosis": data.get("diagnosis") or None,
        "advice": data.get("advice") or None,
    }

def chat(history: list[dict], user_message: str) -> tuple[dict, list[dict]]:
    updated = history + [{"role": "user", "content": user_message}]
    response = _get_client().chat.completions.create(
        model="llama-3.1-8b-instant",
        max_tokens=512,
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + updated,
    )
    raw = response.choices[0].message.content
    result = _parse_response(raw)
    updated.append({"role": "assistant", "content": raw})
    return result, updated
