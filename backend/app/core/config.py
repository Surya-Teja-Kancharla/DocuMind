from pathlib import Path
from typing import Optional
import os

BASE_DIR = Path(__file__).resolve().parents[3]

# --------------------
# File storage
# --------------------
UPLOAD_DIR = BASE_DIR / "data" / "uploads"
PARSED_DIR = BASE_DIR / "data" / "parsed"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
PARSED_DIR.mkdir(parents=True, exist_ok=True)

# --------------------
# File validation
# --------------------
MAX_FILE_SIZE_MB = 20
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".pptx"}

# --------------------
# Deduplication
# --------------------
HASH_REGISTRY_FILE = BASE_DIR / "data" / "hash_registry.txt"
HASH_REGISTRY_FILE.touch(exist_ok=True)

# --------------------
# Redis (session cache)
# --------------------
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# --------------------
# Supabase (chat history – optional at STEP 5)
# --------------------
SUPABASE_URL: Optional[str] = os.getenv("SUPABASE_URL")
SUPABASE_KEY: Optional[str] = os.getenv("SUPABASE_KEY")
