from typing import List
from backend.app.core.config import PARSED_DIR


def load_parsed_documents(chunk_size: int = 1500) -> List[str]:
    """
    Load parsed documents and split into evaluation-sized chunks.
    """
    documents = []

    for file in PARSED_DIR.glob("*.txt"):
        text = file.read_text(encoding="utf-8")
        for i in range(0, len(text), chunk_size):
            documents.append(text[i:i + chunk_size])

    return documents
