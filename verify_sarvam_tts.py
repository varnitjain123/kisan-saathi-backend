import sarvam
import os

print("Testing Sarvam TTS...")
print("Sending Hindi text to Sarvam API...\n")

test_texts = [
    "नमस्ते, मैं KisanSaathi हूँ। आपके टमाटर में क्या समस्या है?",
    "क्या पत्तियों पर कोई धब्बे या कीड़े दिख रहे हैं?",
    "आपके टमाटर में लेट ब्लाइट रोग है। तुरंत मैंकोजेब दवा का छिड़काव करें।",
]

for i, text in enumerate(test_texts, 1):
    print(f"Test {i}: {text[:50]}...")
    audio = sarvam.synthesize(text)
    filename = f"tts_test_{i}.mp3"
    with open(filename, "wb") as f:
        f.write(audio)
    print(f"  ✓ Saved {filename} ({len(audio):,} bytes)")

print("\n✓ TTS working — open each .mp3 file and verify you hear clear Hindi audio.")
print("If audio sounds correct, TTS is ready. Proceed to STT verification.")
