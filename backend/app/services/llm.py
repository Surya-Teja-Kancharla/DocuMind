import os
from typing import Generator
from google import genai

# -----------------------------
# Gemini Configuration
# -----------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set")

client = genai.Client(api_key=GEMINI_API_KEY)

MODEL_NAME = "models/gemini-2.5-flash"


def stream_gemini_response(prompt: str) -> Generator[str, None, None]:
    """
    Stream response tokens from Gemini (chat endpoint).
    Used for /chat/stream.
    """
    response = client.models.generate_content_stream(
        model=MODEL_NAME,
        contents=prompt,
    )

    for chunk in response:
        if chunk.text:
            yield chunk.text


def generate_answer(prompt: str) -> str:
    """
    Non-streaming Gemini response.
    Used for evaluation (RAGAS / offline metrics).
    """
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )
    return response.text.strip()
