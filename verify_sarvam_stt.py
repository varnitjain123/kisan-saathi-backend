import sarvam
import sys
import os

audio_file = "test_audio.wav"

if not os.path.exists(audio_file):
    print(f"✗ File not found: {audio_file}")
    print("  Record a short Hindi sentence and save it as test_audio.wav in this folder.")
    print("  Then re-run this script.")
    sys.exit(1)

print(f"Testing Sarvam STT with {audio_file}...")
with open(audio_file, "rb") as f:
    audio_bytes = f.read()

print(f"Audio file size: {len(audio_bytes):,} bytes")
transcript = sarvam.transcribe(audio_bytes, audio_file)

if transcript:
    print(f"\n✓ STT working!")
    print(f"  Transcript: {transcript}")
    print("\nSarvam STT + TTS both verified. Ready for Step 6.")
else:
    print("\n✗ STT returned empty transcript.")
    print("  Possible causes:")
    print("  - Audio file is silent or too quiet")
    print("  - Wrong file format (use WAV, 16kHz mono if possible)")
    print("  - Sarvam API key issue")
