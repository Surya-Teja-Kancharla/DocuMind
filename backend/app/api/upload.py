from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException, Form
import time
import uuid

from backend.app.core.logging import setup_logger
from backend.app.utils.file_utils import validate_file, validate_file_size
from backend.app.utils.hash_utils import compute_file_hash
from backend.app.utils.file_utils import is_duplicate, register_hash
from backend.app.core.config import UPLOAD_DIR
from backend.app.services.ingestion import ingest_document

logger = setup_logger()
router = APIRouter(prefix="/upload", tags=["Document Upload"])


@router.post("/")
async def upload_document(
    background_tasks: BackgroundTasks,
    session_id: str = Form(...),              # ✅ ADDED
    file: UploadFile = File(...)
):
    start_time = time.time()

    validate_file(file)
    await validate_file_size(file)

    file_path = UPLOAD_DIR / file.filename
    contents = await file.read()

    file_size_mb = round(len(contents) / (1024 * 1024), 2)

    with open(file_path, "wb") as f:
        f.write(contents)

    logger.info(
        f"Upload received | file={file.filename} | size={file_size_mb}MB | session={session_id}"
    )

    file_hash = compute_file_hash(file_path)

    if is_duplicate(file_hash):
        raise HTTPException(status_code=409, detail="Duplicate document")

    register_hash(file_hash)

    document_id = str(uuid.uuid4())

    background_tasks.add_task(
        ingest_document,
        file_path,
        file.filename,
        document_id,
        session_id              # ✅ PASSED
    )

    latency_ms = round((time.time() - start_time) * 1000, 2)

    logger.info(
        f"Upload accepted | document_id={document_id} | session={session_id}"
    )

    return {
        "document_id": document_id,
        "session_id": session_id,
        "status": "processing"
    }
