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
            "question": cleaned or "Could you please describe your problem again?",
            "diagnosis": None,
            "advice": None,
        }
    return {
        "status": data.get("status", "asking"),
        "question": data.get("question") or None,
        "diagnosis": data.get("diagnosis") or None,
        "advice": data.get("advice") or None,
    }


def chat(history: list[dict], user_message: str, location_context: str = "") -> tuple[dict, list[dict]]:
    updated = history + [{"role": "user", "content": user_message}]

    system = SYSTEM_PROMPT
    if location_context:
        system = SYSTEM_PROMPT + "\n\nLOCATION CONTEXT:\n" + location_context

    response = _get_client().chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=512,
        messages=[{"role": "system", "content": system}] + updated,
    )
    raw = response.choices[0].message.content
    result = _parse_response(raw)
    updated.append({"role": "assistant", "content": raw})
    return result, updated
