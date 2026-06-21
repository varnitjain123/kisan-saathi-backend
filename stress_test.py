from engine import chat
import sys
sys.stdout.reconfigure(encoding='utf-8')

TESTS = [
    (
        "1. Late blight (classic)",
        [
            "मेरे टमाटर की पत्तियों पर काले धब्बे हैं",
            "हाँ, पत्तियाँ नीचे से ऊपर की तरफ सूख रही हैं",
            "3-4 दिन से हो रहा है",
            "हाँ, फलों पर भी भूरे धब्बे हैं",
            "हाँ, सफेद फफूंद भी दिख रही है",
        ],
    ),
    (
        "2. Vague input",
        [
            "टमाटर खराब हो रहे हैं",
            "पत्तियाँ पीली हो रही हैं",
            "नई पत्तियाँ ज्यादा पीली हैं",
            "हाँ, छोटे छेद भी दिख रहे हैं",
            "छेद के आसपास काला घेरा है",
        ],
    ),
    (
        "3. Whitefly",
        [
            "पत्तियों के नीचे सफेद कीड़े हैं",
            "पत्तियाँ ऊपर से मुड़ रही हैं",
            "पूरे खेत में फैल गया है",
            "पत्तियां चिपचिपी भी लग रही हैं",
        ],
    ),
    (
        "4. Out of scope — onion question",
        [
            "मुझे प्याज की खेती के बारे में बताओ",
        ],
    ),
    (
        "5. Fruit borer",
        [
            "फल के अंदर कीड़ा है",
            "फल में छेद दिख रहा है बाहर से",
            "कुछ फलों में है, सब में नहीं",
            "हरे और लाल दोनों फलों में छेद है",
        ],
    ),
]


def run_test(label, messages):
    print(f"\n{'='*55}")
    print(f"TEST {label}")
    print('='*55)

    history = []
    warned_early_diagnosis = False

    for i, msg in enumerate(messages):
        print(f"\n  Farmer turn {i+1}: {msg}")
        response, history = chat(history, msg)

        print(f"  Status  : {response['status']}")
        if response['question']:
            print(f"  Question: {response['question']}")
        if response['diagnosis']:
            print(f"  Diagnosis: {response['diagnosis'][:80]}...")
        if response['advice']:
            print(f"  Advice  : {response['advice'][:80]}...")

        if response['status'] == 'asking' and i == 0:
            print("  ✓ Correctly asked a question on turn 1")

        if response['status'] == 'diagnosed' and i == 0 and label != "4. Out of scope — onion question":
            print("  ⚠ WARNING: Diagnosed on first message — Rule 1 violated!")
            warned_early_diagnosis = True

        if response['status'] == 'diagnosed':
            print(f"\n  ✓ Reached diagnosis after {i+1} farmer message(s).")
            return not warned_early_diagnosis

    print(f"\n  ✗ No diagnosis reached in {len(messages)} messages.")
    return False


if __name__ == "__main__":
    print("KisanSaathi Stress Test — 5 conversations\n")
    results = []
    for label, messages in TESTS:
        passed = run_test(label, messages)
        results.append((label, passed))

    print(f"\n{'='*55}")
    print("RESULTS:")
    all_passed = True
    for label, passed in results:
        mark = "✓" if passed else "✗"
        print(f"  {mark} {label}")
        if not passed:
            all_passed = False

    print()
    if all_passed:
        print("✓ All stress tests passed — ready for Step 5 (Sarvam TTS).")
    else:
        print("✗ Fix failing tests before proceeding.")
        print("  Most common fix: strengthen Rule 1 in prompt.py.")
