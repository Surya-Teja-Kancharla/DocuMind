from pathlib import Path
from typing import List, Dict
from backend.app.services.llm import generate_answer

PARSED_DIR = Path("data/parsed")


def generate_qa_pairs_for_document(
    document_id: str,
    num_questions: int = 5,
    chunk_size: int = 1500
) -> List[Dict]:
    """
    Generate evaluation-ready QA pairs for a single document.

    Output format is RAGAS-compatible:
    {
        question: str,
        answer: str,
        contexts: List[str]
    }
    """

    doc_path = PARSED_DIR / f"{document_id}.txt"
    if not doc_path.exists():
        return []

    text = doc_path.read_text(encoding="utf-8")

    # Split document into chunks for context grounding
    chunks = [
        text[i:i + chunk_size]
        for i in range(0, len(text), chunk_size)
    ]

    question_prompt = f"""
    You are generating evaluation questions for a Retrieval-Augmented Generation (RAG) system.

    From the document below, generate {num_questions}
    clear, factual, non-overlapping questions that can be
    answered directly using the document content.

    Return ONLY a numbered list of questions.
    """

    questions_text = generate_answer(
        question_prompt + "\n\n" + text[:4000]
    )

    questions = [
        q.strip().lstrip("0123456789. ").strip()
        for q in questions_text.split("\n")
        if q.strip()
    ][:num_questions]

    qa_pairs = []

    for question in questions:
        answer_prompt = f"""
        Answer the following question using ONLY the information
        present in the document context. Do not add external knowledge.

        Question:
        {question}

        Document Context:
        {text[:4000]}
        """

        answer = generate_answer(answer_prompt)

        qa_pairs.append({
            "question": question,
            "answer": answer.strip(),
            "contexts": chunks[:5]  # limit for token control
        })

    return qa_pairs


def generate_qa_pairs_batch(
    document_ids: List[str],
    num_questions: int = 5
) -> List[Dict]:
    """
    Generate QA pairs across multiple documents.
    Used for batch offline evaluation.
    """

    dataset = []

    for doc_id in document_ids:
        dataset.extend(
            generate_qa_pairs_for_document(
                document_id=doc_id,
                num_questions=num_questions
            )
        )

    return dataset
