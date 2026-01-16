import os
from typing import AsyncGenerator
from openai import AsyncOpenAI

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is not set")

client = AsyncOpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)

MODEL_NAME = "llama-3.1-8b-instant"


async def stream_llm_response(prompt: str) -> AsyncGenerator[str, None]:
    """
    STEP 7: Async token streaming from Groq.
    """

    stream = await client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
        temperature=0.2,
    )

    async for chunk in stream:
        delta = chunk.choices[0].delta
        if delta and delta.content:
            yield delta.content
