from dotenv import load_dotenv
import os

load_dotenv()

anthropic_ok = bool(os.environ.get("ANTHROPIC_API_KEY"))
sarvam_ok = bool(os.environ.get("SARVAM_API_KEY"))

print("ANTHROPIC_API_KEY:", "✓ found" if anthropic_ok else "✗ MISSING")
print("SARVAM_API_KEY:   ", "✓ found" if sarvam_ok else "✗ MISSING")

if anthropic_ok and sarvam_ok:
    print("\nSetup OK — ready to proceed to Step 2.")
else:
    print("\nFix .env before continuing. Do not proceed until both keys show ✓.")
