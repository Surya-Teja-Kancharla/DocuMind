import time
from pathlib import Path

from llama_index.core import Document

from backend.app.core.config import PARSED_DIR
from backend.app.core.logging import setup_logger

from pypdf import PdfReader
from docx import Document as DocxDocument
from pptx import Presentation

logger = setup_logger()


def parse_file(file_path: Path) -> str:
    """
    Parse supported document formats into raw text.
    """

    ext = file_path.suffix.lower()

    if ext == ".pdf":
        reader = PdfReader(str(file_path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    if ext == ".docx":
        doc = DocxDocument(str(file_path))
        return "\n".join(p.text for p in doc.paragraphs)

    if ext == ".pptx":
        prs = Presentation(str(file_path))
        slides_text = []
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    slides_text.append(shape.text)
        return "\n".join(slides_text)

    raise ValueError("Unsupported file format")


def ingest_document(
    file_path: Path,
    original_filename: str,
    document_id: str
) -> None:
    """
    Background ingestion with observability & metrics.

    Responsibilities:
    - Parse document into machine-readable text
    - Create LlamaIndex Document abstraction
    - Persist parsed text for audit/debug
    - Log parsing duration and ingestion status

    NOTE:
    - No return values
    - No UUID generation
    """

    logger.info(
        f"Parsing started | document_id={document_id} | file={original_filename}"
    )

    start_time = time.time()

    try:
        parsed_text = parse_file(file_path)

        duration_ms = round((time.time() - start_time) * 1000, 2)

        # LlamaIndex document creation (handoff to RAG pipeline)
        Document(
            text=parsed_text,
            metadata={
                "document_id": document_id,
                "filename": original_filename
            }
        )

        # Persist parsed output
        parsed_output_path = PARSED_DIR / f"{document_id}.txt"
        parsed_output_path.write_text(parsed_text, encoding="utf-8")

        logger.info(
            f"Parsing completed | document_id={document_id} | "
            f"duration_ms={duration_ms} | status=success"
        )

    except Exception as e:
        duration_ms = round((time.time() - start_time) * 1000, 2)

        logger.error(
            f"Parsing failed | document_id={document_id} | "
            f"duration_ms={duration_ms} | reason={str(e)}"
        )
