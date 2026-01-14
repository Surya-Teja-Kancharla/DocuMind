import os
from google import genai

# Fetch the key from your system environment variables
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY environment variable not set.")
else:
    client = genai.Client(api_key=api_key)

    print("Available models:")
    # This will now work without the 400 error
    for model in client.models.list():
        print(f"- {model.name}")