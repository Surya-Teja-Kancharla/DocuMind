from backend.app.core.config import SUPABASE_CLIENT


def store_chat_message(
    user_id: str,
    session_id: str,
    role: str,
    content: str
):
    SUPABASE_CLIENT.table("chat_history").insert({
        "user_id": user_id,
        "session_id": session_id,
        "role": role,
        "content": content
    }).execute()
