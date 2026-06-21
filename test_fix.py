import requests
import json

BASE = "http://localhost:8000"

r = requests.post(f"{BASE}/chat/text", json={"session_id": "test-fix-1", "message": "मेरे टमाटर की पत्तियों पर काले धब्बे हैं"})
data = r.json()
print(json.dumps(data, ensure_ascii=False, indent=2))

if data["status"] == "asking":
    print("\n✓ FIXED — correctly asked a question instead of diagnosing")
else:
    print("\n✗ STILL BROKEN — diagnosed on first message")
