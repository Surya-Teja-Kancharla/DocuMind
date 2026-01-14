from typing import List
from llama_index.core.schema import TextNode

from backend.app.core.prompts import RAG_CONTEXT_PROMPT


MAX_RECENT_MESSAGES = 4
MAX_CHUNKS = 5


def summarize_conversation(messages: List[str]) -> str:
    """
    Deterministic conversation summarizer.
    (LLM-based summarization deferred to STEP 7)
    """

    if not messages:
        return "No prior conversation."

    if len(messages) <= MAX_RECENT_MESSAGES:
        return "Conversation ongoing. No summary required."

    older_messages = messages[:-MAX_RECENT_MESSAGES]
    return "Earlier discussion topics: " + " | ".join(older_messages[-3:])


def assemble_context(
    user_query: str,
    retrieved_nodes: List[TextNode],
    conversation_messages: List[str]
) -> str:
    """
    Assemble the final RAG context prompt.
    """

    conversation_summary = summarize_conversation(conversation_messages)

    recent_messages = "\n".join(
        conversation_messages[-MAX_RECENT_MESSAGES:]
    )

    retrieved_context = "\n\n".join(
        f"[Source {i+1}]\n{node.text}"
        for i, node in enumerate(retrieved_nodes[:MAX_CHUNKS])
    )

    return RAG_CONTEXT_PROMPT.format(
        conversation_summary=conversation_summary,
        recent_messages=recent_messages or "No recent messages.",
        retrieved_context=retrieved_context or "No relevant documents found.",
        user_query=user_query
    )
