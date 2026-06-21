import httpx

print("--- TEST B ---")
resp_b = httpx.post("http://localhost:8000/chat/text", json={
  "session_id": "test-farmer-1",
  "message": "मेरे टमाटर की पत्तियों पर काले धब्बे हैं"
}, timeout=30)
print(resp_b.json())

print("\n--- TEST C ---")
resp_c = httpx.post("http://localhost:8000/chat/text", json={
  "session_id": "test-farmer-1",
  "message": "हाँ, पत्तियाँ नीचे से सूख रही हैं"
}, timeout=30)
print(resp_c.json())

print("\n--- TEST D ---")
resp_d = httpx.post("http://localhost:8000/chat/speak", json={
  "text": "क्या पत्तियों पर कोई धब्बे या कीड़े दिख रहे हैं?"
}, timeout=30)
if resp_d.status_code == 200 and resp_d.headers.get("content-type") == "audio/mpeg":
    print("SUCCESS: Received audio/mpeg")
else:
    print(f"FAILED: status={resp_d.status_code}, content-type={resp_d.headers.get('content-type')}")

print("\n--- TEST E ---")
resp_e = httpx.post("http://localhost:8000/chat/text", json={
  "session_id": "test-farmer-2",
  "message": "फल के अंदर कीड़ा है"
}, timeout=30)
print(resp_e.json())
