from typing import List, Dict  # Added Dict here
from llama_index.core.schema import TextNode
from backend.app.core.prompts import RAG_CONTEXT_PROMPT

MAX_RECENT_MESSAGES = 4
MAX_CHUNKS = 5


def format_message(msg: Dict[str, str]) -> str:
    """Helper to convert message dict to formatted string."""
    return f"{msg.get('role', 'unknown')}: {msg.get('content', '')}"


def summarize_conversation(messages: List[Dict[str, str]]) -> str:
    """
    Deterministic conversation summarizer.
    Updated to handle a list of message dictionaries.
    """
    if not messages:
        return "No prior conversation."

    if len(messages) <= MAX_RECENT_MESSAGES:
        return "Conversation ongoing. No summary required."

    # Convert dictionaries to strings before joining
    older_messages = [format_message(m) for m in messages[:-MAX_RECENT_MESSAGES]]
    return "Earlier discussion topics: " + " | ".join(older_messages[-3:])


def assemble_context(
    user_query: str,
    retrieved_nodes: List[TextNode],
    conversation_messages: List[Dict[str, str]]  # Updated to List[Dict]
) -> str:
    """
    Assemble the final RAG context prompt.
    """
    conversation_summary = summarize_conversation(conversation_messages)

    # Convert message dicts to strings before joining to avoid TypeError
    recent_messages = "\n".join(
        format_message(m) for m in conversation_messages[-MAX_RECENT_MESSAGES:]
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
