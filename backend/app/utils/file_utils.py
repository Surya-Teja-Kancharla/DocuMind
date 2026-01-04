from fastapi import UploadFile, HTTPException
from backend.app.core.config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE_MB
from backend.app.core.config import HASH_REGISTRY_FILE


def validate_file(file: UploadFile):
    ext = "." + file.filename.split(".")[-1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {ext}"
        )

    return ext


async def validate_file_size(file: UploadFile):
    contents = await file.read()
    size_mb = len(contents) / (1024 * 1024)

    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=400,
            detail="File exceeds maximum size limit"
        )

    await file.seek(0)


def is_duplicate(file_hash: str) -> bool:
    hashes = HASH_REGISTRY_FILE.read_text().splitlines()
    return file_hash in hashes


def register_hash(file_hash: str):
    with open(HASH_REGISTRY_FILE, "a") as f:
        f.write(file_hash + "\n")
