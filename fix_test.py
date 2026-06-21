import requests
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = "http://localhost:8000"

r = requests.post(f"{BASE}/chat/text", json={"session_id": "test-fix-1", "message": "मेरे टमाटर की पत्तियों पर काले धब्बे हैं"})
data = r.json()
print(json.dumps(data, ensure_ascii=False, indent=2))

if data["status"] == "asking":
    print("FIXED — correctly asked a question")
else:
    print("STILL BROKEN — diagnosed on first message")
