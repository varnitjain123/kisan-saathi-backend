from prompt import SYSTEM_PROMPT

checks = {
    "Contains 'asking'": "asking" in SYSTEM_PROMPT,
    "Contains 'diagnosed'": "diagnosed" in SYSTEM_PROMPT,
    "Contains 'Hindi'": "Hindi" in SYSTEM_PROMPT,
    "Contains output format instructions": "OUTPUT FORMAT" in SYSTEM_PROMPT,
    "Contains rule about first message": "first message" in SYSTEM_PROMPT,
    "Long enough (>500 chars)": len(SYSTEM_PROMPT) > 500,
}

all_passed = True
for check, result in checks.items():
    status = "✓" if result else "✗"
    print(f"  {status} {check}")
    if not result:
        all_passed = False

print()
if all_passed:
    print("prompt.py ✓ all checks passed — ready for Step 3.")
else:
    print("✗ Some checks failed. Do not proceed. Fix prompt.py and re-run.")
