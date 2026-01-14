from supabase import create_client
from backend.app.core.config import SUPABASE_URL, SUPABASE_KEY


def get_supabase_client():
    if not SUPABASE_URL or not SUPABASE_KEY:
        # STEP 5–7 safe: Supabase optional
        return None
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def store_chat_message(
    user_id: str,
    session_id: str,
    role: str,
    content: str
):
    client = get_supabase_client()
    if client is None:
        # Supabase not configured yet — safely skip
        return

    client.table("chat_history").insert({
        "user_id": user_id,
        "session_id": session_id,
        "role": role,
        "content": content
    }).execute()
