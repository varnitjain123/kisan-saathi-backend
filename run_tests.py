import requests
import json

BASE = "http://localhost:8000"

print("=== Test B ===")
r = requests.post(f"{BASE}/chat/text", json={"session_id": "test-farmer-1", "message": "मेरे टमाटर की पत्तियों पर काले धब्बे हैं"})
print(json.dumps(r.json(), ensure_ascii=False, indent=2))

print("\n=== Test C ===")
r = requests.post(f"{BASE}/chat/text", json={"session_id": "test-farmer-1", "message": "हाँ, पत्तियाँ नीचे से ऊपर की तरफ सूख रही हैं"})
print(json.dumps(r.json(), ensure_ascii=False, indent=2))

print("\n=== Test D ===")
r = requests.post(f"{BASE}/chat/speak", json={"text": "क्या पत्तियों पर कोई धब्बे या कीड़े दिख रहे हैं?"})
print(f"Audio received: {len(r.content)} bytes, content-type: {r.headers.get('content-type')}")

print("\n=== Test E ===")
r = requests.post(f"{BASE}/chat/text", json={"session_id": "test-farmer-2", "message": "फल के अंदर कीड़ा है"})
print(json.dumps(r.json(), ensure_ascii=False, indent=2))
