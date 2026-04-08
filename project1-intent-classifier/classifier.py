from groq import Groq

import os
API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=API_KEY)

def classify_intent(command):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": f"""Classify this voice command into exactly one of these intents:
                climate_control, media_control, navigation, phone_call, general_query

                Voice command: "{command}"

                Reply with only the intent name, nothing else."""
            }
        ]
    )
    return response.choices[0].message.content.strip()

# Test with 10 sample commands
test_commands = [
    "Turn on the AC",
    "Play some jazz music",
    "Take me to the airport",
    "Call mom",
    "What's the weather today",
    "Set temperature to 22 degrees",
    "Skip this song",
    "Navigate to Berlin city center",
    "Call John",
    "Turn off the heating"
]

print("Voice Command Intent Classifier")
print("=" * 40)

for command in test_commands:
    intent = classify_intent(command)
    print(f"Command: {command}")
    print(f"Intent:  {intent}")
    print("-" * 40)