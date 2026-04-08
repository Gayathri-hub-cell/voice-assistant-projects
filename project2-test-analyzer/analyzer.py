import json
import os
from groq import Groq

API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=API_KEY)

def load_test_results(filename):
    with open(filename, "r") as f:
        return json.load(f)

def analyze_failures(results):
    failed_tests = [r for r in results if r["status"] == "FAIL"]
    passed_tests = [r for r in results if r["status"] == "PASS"]
    return failed_tests, passed_tests

def get_ai_summary(failed_tests):
    failures_text = "\n".join([
        f"- Test {t['test_id']}: Command '{t['command']}' expected '{t['expected']}' but got '{t['actual']}'"
        for t in failed_tests
    ])
    
    prompt = f"""You are a QA engineer analyzing voice assistant test failures.
    
Here are the failed tests:
{failures_text}

Please provide:
1. A brief summary of what went wrong
2. The most likely root cause
3. One suggestion to fix it

Keep your response short and clear."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def main():
    data = load_test_results("test_results.json")
    
    print(f"Test Run: {data['test_run']}")
    print(f"Date: {data['date']}")
    print("=" * 50)
    
    failed, passed = analyze_failures(data["results"])
    
    print(f"Total Tests: {len(data['results'])}")
    print(f"Passed: {len(passed)}")
    print(f"Failed: {len(failed)}")
    print("=" * 50)
    
    if failed:
        print("\nFailed Tests:")
        for t in failed:
            print(f"  {t['test_id']}: '{t['command']}' → expected {t['expected']}, got {t['actual']}")
        
        print("\nAI Analysis:")
        print("-" * 50)
        summary = get_ai_summary(failed)
        print(summary)
    else:
        print("All tests passed!")

main()