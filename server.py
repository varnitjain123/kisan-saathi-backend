from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel
from typing import Optional
import engine
import sarvam
import vision
from geo import get_location_context

app = FastAPI(title="KisanSaathi Engine", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_sessions: dict[str, list[dict]] = {}


def _get_or_create(session_id: str):
    if session_id not in _sessions:
        _sessions[session_id] = []
    return _sessions[session_id]


class TextTurnRequest(BaseModel):
    session_id: str
    message: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class TurnResponse(BaseModel):
    session_id: str
    status: str
    question: Optional[str]
    diagnosis: Optional[str]
    advice: Optional[str]


class SpeakRequest(BaseModel):
    text: str


@app.post("/chat/text", response_model=TurnResponse)
def chat_text(body: TextTurnRequest):
    history = _get_or_create(body.session_id)

    location_context = ""
    if body.latitude is not None and body.longitude is not None:
        location_context = get_location_context(body.latitude, body.longitude)

    try:
        response, updated = engine.chat(history, body.message, location_context)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LLM error: {e}")

    _sessions[body.session_id] = updated
    return TurnResponse(session_id=body.session_id, **response)


@app.post("/chat/image", response_model=TurnResponse)
async def chat_image(
    session_id: str = Form(...),
    message: str = Form(...),
    image: UploadFile = File(...),
    latitude: Optional[float] = Form(None),
    longitude: Optional[float] = Form(None),
):
    image_bytes = await image.read()

    try:
        image_context = vision.analyze_image(image_bytes)
    except Exception:
        image_context = ""

    location_context = ""
    if latitude is not None and longitude is not None:
        location_context = get_location_context(latitude, longitude)

    combined_context = " | ".join(filter(None, [image_context, location_context]))

    history = _get_or_create(session_id)
    try:
        response, updated = engine.chat(history, message, combined_context)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LLM error: {e}")

    _sessions[session_id] = updated
    return TurnResponse(session_id=session_id, **response)


@app.post("/chat/voice", response_model=TurnResponse)
async def chat_voice(session_id: str, audio: UploadFile = File(...)):
    audio_bytes = await audio.read()

    try:
        transcript = sarvam.transcribe(audio_bytes, audio.filename or "audio.wav")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"STT error: {e}")

    if not transcript:
        raise HTTPException(status_code=422, detail="Could not transcribe audio.")

    history = _get_or_create(session_id)
    try:
        response, updated = engine.chat(history, transcript)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LLM error: {e}")

    _sessions[session_id] = updated
    return TurnResponse(session_id=session_id, **response)


@app.post("/chat/speak")
def speak(body: SpeakRequest):
    try:
        audio_bytes = sarvam.synthesize(body.text)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"TTS error: {e}")
    return Response(content=audio_bytes, media_type="audio/mpeg")


@app.delete("/session/{session_id}")
def clear_session(session_id: str):
    _sessions.pop(session_id, None)
    return {"cleared": session_id}


@app.get("/health")
def health():
    return {"status": "ok", "sessions_active": len(_sessions)}
