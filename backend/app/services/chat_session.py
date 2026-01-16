from typing import List, Dict
from backend.app.core.redis import get_redis_client
import logging

logger = logging.getLogger(__name__)

SESSION_TTL_SECONDS = 3600
MAX_CONTEXT_MESSAGES = 6

REDIS_SESSION_PREFIX = "chat:session:"


def _session_key(session_id: str) -> str:
    return f"{REDIS_SESSION_PREFIX}{session_id}"


def append_session_message(session_id: str, role: str, content: str):
    redis_client = get_redis_client()
    if not redis_client:
        return

    key = _session_key(session_id)

    try:
        redis_client.rpush(key, f"{role}:{content}")
        redis_client.ltrim(key, -MAX_CONTEXT_MESSAGES, -1)
        redis_client.expire(key, SESSION_TTL_SECONDS)
    except Exception as e:
        logger.error(f"Redis write failed: {e}")


def get_session_messages(session_id: str) -> List[Dict[str, str]]:
    redis_client = get_redis_client()
    if not redis_client:
        return []

    key = _session_key(session_id)

    try:
        messages = redis_client.lrange(key, 0, -1)
    except Exception as e:
        logger.error(f"Redis read failed: {e}")
        return []

    decoded = []
    for msg in messages:
        role, content = msg.split(":", 1)
        decoded.append({"role": role, "content": content})

    return decoded
