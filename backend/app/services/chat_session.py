from typing import List
from backend.app.core.redis import redis_client

SESSION_TTL_SECONDS = 3600
MAX_CONTEXT_MESSAGES = 6


def get_session_messages(session_id: str) -> List[str]:
    messages = redis_client.lrange(session_id, 0, -1)
    return messages[-MAX_CONTEXT_MESSAGES:]


def append_session_message(session_id: str, message: str):
    redis_client.rpush(session_id, message)
    redis_client.expire(session_id, SESSION_TTL_SECONDS)
