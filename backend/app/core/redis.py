import redis
from backend.app.core.config import REDIS_URL

def get_redis_client():
    try:
        client = redis.Redis.from_url(
            REDIS_URL,
            decode_responses=True,
            socket_connect_timeout=1
        )
        client.ping()
        return client
    except Exception:
        return None
