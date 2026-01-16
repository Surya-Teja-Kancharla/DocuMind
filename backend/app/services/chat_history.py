from backend.app.core.config import get_supabase_client
import logging

logger = logging.getLogger(__name__)


def store_chat_message(
    user_id: str,
    session_id: str,
    role: str,
    content: str
):
    """
    Durably persist chat messages to Supabase.
    Fail soft, but never silently.
    """
    client = get_supabase_client()
    if not client:
        logger.warning("Supabase unavailable — chat message not persisted")
        return

    try:
        client.table("chat_messages").insert({
            "user_id": user_id,
            "session_id": session_id,
            "role": role,
            "content": content
        }).execute()
    except Exception as e:
        logger.error(f"Supabase insert failed: {e}")


def fetch_chat_history(session_id: str, limit: int = 20):
    """
    Fetch persisted chat history.
    """
    client = get_supabase_client()
    if not client:
        return []

    try:
        response = (
            client
            .table("chat_messages")
            .select("role, content")
            .eq("session_id", session_id)
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )
        return list(reversed(response.data)) if response.data else []
    except Exception as e:
        logger.error(f"Supabase fetch failed: {e}")
        return []
