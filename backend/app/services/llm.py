import os
from typing import Generator

from google import genai

# Gemini configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set")

client = genai.Client(api_key=GEMINI_API_KEY)


def stream_gemini_response(prompt: str) -> Generator[str, None, None]:
    """
    Stream response tokens from Gemini using the new google.genai SDK.
    """

    response = client.models.generate_content_stream(
        model="models/gemini-2.5-flash",
        contents=prompt,
    )

    for chunk in response:
        if chunk.text:
            yield chunk.text
