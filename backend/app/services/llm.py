import os
from typing import Generator
from openai import OpenAI

# -----------------------------
# Groq Configuration
# -----------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is not set")

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)

# Recommended Groq models
MODEL_NAME = "llama-3.1-8b-instant"
# Alternatives:
# "llama3-8b-8192"
# "mixtral-8x7b-32768"


def stream_llm_response(prompt: str) -> Generator[str, None, None]:
    """
    Stream response tokens from Groq.
    Used for /chat/stream.
    """
    stream = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
        temperature=0.2,
    )

    for chunk in stream:
        delta = chunk.choices[0].delta
        if delta and delta.content:
            yield delta.content


def generate_answer(prompt: str) -> str:
    """
    Non-streaming Groq response.
    Used for evaluation / QA generation.
    """
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return response.choices[0].message.content.strip()
