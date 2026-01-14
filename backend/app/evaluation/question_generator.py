import os
from typing import List
from google.genai import Client

# Gemini client
client = Client(api_key=os.environ["GEMINI_API_KEY"])


def generate_questions(context: str, n: int = 3) -> List[str]:
    """
    Generate factual, document-grounded questions from context.
    """
    prompt = f"""
    You are generating evaluation questions for a RAG system.

    From the following document content, generate {n}
    clear, factual, answerable questions.

    Content:
    {context}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    questions = []
    for line in response.text.split("\n"):
        line = line.strip()
        if line and not line.lower().startswith(("sure", "here")):
            questions.append(line.lstrip("- ").strip())

    return questions[:n]


def generate_reference_answer(question: str, context: str) -> str:
    """
    Generate a ground-truth answer strictly from document context.
    """
    prompt = f"""
    Answer the following question using ONLY the information
    present in the provided context. Do not add external knowledge.

    Question:
    {question}

    Context:
    {context}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text.strip()
