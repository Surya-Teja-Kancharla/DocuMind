# backend/app/core/config.py
from pathlib import Path
import os
from dotenv import load_dotenv
from supabase import create_client
from typing import Optional

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[3]

UPLOAD_DIR = BASE_DIR / "data" / "uploads"
PARSED_DIR = BASE_DIR / "data" / "parsed"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
PARSED_DIR.mkdir(parents=True, exist_ok=True)

MAX_FILE_SIZE_MB = 20
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".pptx"}

HASH_REGISTRY_FILE = BASE_DIR / "data" / "hash_registry.txt"
HASH_REGISTRY_FILE.touch(exist_ok=True)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

_supabase_client: Optional[object] = None


def get_supabase_client():
    """
    Lazily initialize Supabase client with health check.
    """
    global _supabase_client

    if _supabase_client is not None:
        return _supabase_client

    if not SUPABASE_URL or not SUPABASE_KEY:
        return None

    try:
        client = create_client(SUPABASE_URL, SUPABASE_KEY)
        # Lightweight health check
        client.table("chat_messages").select("id").limit(1).execute()
        _supabase_client = client
        return client
    except Exception:
        return None
