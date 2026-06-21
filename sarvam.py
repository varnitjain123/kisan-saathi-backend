import os
import base64
import httpx
from dotenv import load_dotenv

load_dotenv()

SARVAM_API_KEY = os.environ.get("SARVAM_API_KEY", "")
STT_URL = "https://api.sarvam.ai/speech-to-text"
TTS_URL = "https://api.sarvam.ai/text-to-speech"
HEADERS = {"api-subscription-key": SARVAM_API_KEY}


def transcribe(audio_bytes: bytes, filename: str = "audio.wav") -> str:
    """
    Convert audio bytes to Hindi text.
    Accepts WAV, MP3, OGG, WEBM.
    Returns transcribed string. Returns empty string if inaudible.
    """
    files = {"file": (filename, audio_bytes, "audio/wav")}
    data = {"language_code": "hi-IN", "model": "saarika:v2.5"}

    resp = httpx.post(STT_URL, headers=HEADERS, files=files, data=data, timeout=30)
    if resp.status_code != 200:
        print(f"Error from STT API: {resp.text}")
    resp.raise_for_status()
    return resp.json().get("transcript", "").strip()


def synthesize(text: str) -> bytes:
    """
    Convert Hindi text to MP3 audio bytes.
    Returns raw MP3 bytes — caller writes to file or streams directly.
    """
    payload = {
        "inputs": [text],
        "target_language_code": "hi-IN",
        "speaker": "priya",
        "model": "bulbul:v3",
        "enable_preprocessing": True,
    }

    resp = httpx.post(
        TTS_URL,
        headers={**HEADERS, "Content-Type": "application/json"},
        json=payload,
        timeout=30,
    )
    if resp.status_code != 200:
        print(f"Error from TTS API: {resp.text}")
    resp.raise_for_status()

    audios = resp.json().get("audios", [])
    if not audios:
        raise ValueError(f"Sarvam TTS returned no audio. Full response: {resp.json()}")

    return base64.b64decode(audios[0])
