from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]

UPLOAD_DIR = BASE_DIR / "data" / "uploads"
PARSED_DIR = BASE_DIR / "data" / "parsed"

MAX_FILE_SIZE_MB = 20
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".pptx"}

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
PARSED_DIR.mkdir(parents=True, exist_ok=True)

HASH_REGISTRY_FILE = BASE_DIR / "data" / "hash_registry.txt"
HASH_REGISTRY_FILE.touch(exist_ok=True)
