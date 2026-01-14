# backend/app/services/chat_history.py
from backend.app.core.config import get_supabase_client


def store_chat_message(
    user_id: str,
    session_id: str,
    role: str,
    content: str
):
    """
    Persist a chat message if Supabase is available.
    Fail silently if offline.
    """
    client = get_supabase_client()
    if not client:
        return

    try:
        client.table("chat_messages").insert({
            "user_id": user_id,
            "session_id": session_id,
            "role": role,
            "content": content
        }).execute()
    except Exception:
        # Silent failure (fallback mode)
        pass


def fetch_chat_history(session_id: str, limit: int = 20):
    """
    Fetch chat history if Supabase is available.
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
    except Exception:
        return []
