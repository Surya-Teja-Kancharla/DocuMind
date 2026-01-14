from typing import List
from datasets import Dataset
from pathlib import Path

from backend.app.evaluation.qa_generator import generate_qa_pairs_batch


PARSED_DIR = Path("data/parsed")


def build_evaluation_dataset(
    num_questions_per_doc: int = 3
) -> Dataset:
    """
    Build a dynamic, document-grounded evaluation dataset
    for RAGAS using parsed documents.
    """

    document_ids = [
        file.stem
        for file in PARSED_DIR.glob("*.txt")
    ]

    qa_samples = generate_qa_pairs_batch(
        document_ids=document_ids,
        num_questions=num_questions_per_doc
    )

    if not qa_samples:
        raise RuntimeError("No evaluation samples generated")

    data = {
        "question": [],
        "answer": [],
        "contexts": []
    }

    for sample in qa_samples:
        data["question"].append(sample["question"])
        data["answer"].append(sample["answer"])
        data["contexts"].append(sample["contexts"])

    return Dataset.from_dict(data)
