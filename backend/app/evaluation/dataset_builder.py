from typing import List
from backend.app.core.config import get_supabase_client, PARSED_DIR
from backend.app.evaluation.schemas import EvaluationSample


def load_parsed_contexts(document_id: str) -> List[str]:
    path = PARSED_DIR / f"{document_id}.txt"
    if not path.exists():
        return []

    text = path.read_text(encoding="utf-8")
    return [text[i:i+1500] for i in range(0, len(text), 1500)]


def build_evaluation_dataset(limit: int = 20) -> List[EvaluationSample]:
    client = get_supabase_client()
    if not client:
        raise RuntimeError("Supabase not available for evaluation")

    rows = (
        client.table("chat_messages")
        .select("session_id, role, content")
        .order("created_at", desc=True)
        .limit(limit * 2)
        .execute()
        .data
    )

    dataset = []
    current_q = None

    for row in reversed(rows):
        if row["role"] == "user":
            current_q = row["content"]

        elif row["role"] == "assistant" and current_q:
            # NOTE: You can improve this by storing document_id per session later
            contexts = []
            for file in PARSED_DIR.glob("*.txt"):
                contexts.extend(load_parsed_contexts(file.stem))

            dataset.append(
                EvaluationSample(
                    question=current_q,
                    answer=row["content"],
                    contexts=contexts[:5]
                )
            )
            current_q = None

    return dataset
