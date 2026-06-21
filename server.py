from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel
from typing import Optional
import engine
import sarvam

app = FastAPI(title="KisanSaathi Engine", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session store: { session_id: [history turns] }
# For production, replace with Redis. Interface stays identical.
_sessions: dict[str, list[dict]] = {}


def _get_or_create(session_id: str) -> list[dict]:
    if session_id not in _sessions:
        _sessions[session_id] = []
    return _sessions[session_id]


# ── Request / Response models ─────────────────────────────────────────────────

class TextTurnRequest(BaseModel):
    session_id: str
    message: str


class TurnResponse(BaseModel):
    session_id: str
    status: str
    question: Optional[str]
    diagnosis: Optional[str]
    advice: Optional[str]


class SpeakRequest(BaseModel):
    text: str


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.post("/chat/text", response_model=TurnResponse)
def chat_text(body: TextTurnRequest):
    """
    Text turn. Person B's primary integration endpoint.
    Send farmer's message as text, receive structured JSON.
    """
    history = _get_or_create(body.session_id)
    try:
        response, updated = engine.chat(history, body.message)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LLM error: {e}")
    _sessions[body.session_id] = updated
    return TurnResponse(session_id=body.session_id, **response)


@app.post("/chat/voice", response_model=TurnResponse)
async def chat_voice(session_id: str, audio: UploadFile = File(...)):
    """
    Voice turn. Upload audio file as multipart form data.
    session_id passed as query param: /chat/voice?session_id=farmer-123
    Audio is transcribed via Sarvam STT, then passed to LLM engine.
    Accepts WAV, MP3, OGG, WEBM.
    """
    audio_bytes = await audio.read()

    try:
        transcript = sarvam.transcribe(audio_bytes, audio.filename or "audio.wav")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"STT error: {e}")

    if not transcript:
        raise HTTPException(
            status_code=422,
            detail="Could not transcribe audio. Please speak clearly and try again."
        )

    history = _get_or_create(session_id)
    try:
        response, updated = engine.chat(history, transcript)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LLM error: {e}")

    _sessions[session_id] = updated
    return TurnResponse(session_id=session_id, **response)


@app.post("/chat/speak")
def speak(body: SpeakRequest):
    """
    TTS utility. Pass Hindi text, receive MP3 audio.
    Person B calls this to play questions/diagnosis back to the farmer.
    Returns: audio/mpeg binary stream.
    """
    try:
        audio_bytes = sarvam.synthesize(body.text)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"TTS error: {e}")
    return Response(content=audio_bytes, media_type="audio/mpeg")


@app.delete("/session/{session_id}")
def clear_session(session_id: str):
    """Reset conversation history. Call this to start a fresh conversation."""
    _sessions.pop(session_id, None)
    return {"cleared": session_id}


@app.get("/health")
def health():
    return {"status": "ok", "sessions_active": len(_sessions)}
