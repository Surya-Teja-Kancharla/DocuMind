# backend/app/services/chat_session.py
from typing import List, Dict
from backend.app.core.redis import redis_client

SESSION_TTL_SECONDS = 3600
MAX_CONTEXT_MESSAGES = 6


def append_session_message(session_id: str, role: str, content: str):
    redis_client.rpush(session_id, f"{role}:{content}")
    redis_client.expire(session_id, SESSION_TTL_SECONDS)


def get_session_messages(session_id: str) -> List[Dict[str, str]]:
    messages = redis_client.lrange(session_id, -MAX_CONTEXT_MESSAGES, -1)
    decoded = []

    for msg in messages:
        role, content = msg.decode().split(":", 1)
        decoded.append({"role": role, "content": content})

    return decoded
