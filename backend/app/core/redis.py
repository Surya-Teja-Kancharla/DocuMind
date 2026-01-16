import redis
from backend.app.core.config import REDIS_URL
import logging

logger = logging.getLogger(__name__)

_redis_client = None


def get_redis_client():
    global _redis_client

    if _redis_client:
        return _redis_client

    try:
        client = redis.Redis.from_url(
            REDIS_URL,
            decode_responses=True,
            socket_connect_timeout=1
        )
        client.ping()
        _redis_client = client
        return client
    except Exception as e:
        logger.warning(f"Redis unavailable: {e}")
        return None
