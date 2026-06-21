from engine import chat

print("Making real API call to Claude...")
print("Sending: 'मेरे टमाटर की पत्तियों पर काले धब्बे हैं'\n")

response, history = chat([], "मेरे टमाटर की पत्तियों पर काले धब्बे हैं")

print(f"Status   : {response['status']}")
print(f"Question : {response['question']}")
print(f"Diagnosis: {response['diagnosis']}")
print(f"Advice   : {response['advice']}")
print()

# Assertions
errors = []
if response['status'] != 'asking':
    errors.append("✗ FAIL: status should be 'asking' on first message (Rule 1 violated)")
if response['question'] is None:
    errors.append("✗ FAIL: question should not be null on first turn")
if response['diagnosis'] is not None:
    errors.append("✗ FAIL: diagnosis must be null when status is 'asking'")
if response['question'] and not any(c > '\u0900' for c in response['question']):
    errors.append("✗ FAIL: question does not appear to be in Hindi (Devanagari)")

if errors:
    for e in errors:
        print(e)
    print("\nDo not proceed. Fix the issue and re-run.")
else:
    print("engine.py ✓ working correctly:")
    print("  - Did not diagnose on first message")
    print("  - Returned a Hindi question")
    print("  - Output contract shape is correct")
    print("\nReady for Step 4.")
