from datetime import datetime

from backend.app.services.chunking import chunk_document
from backend.app.services.embeddings import generate_embeddings
from backend.app.services.vector_store import get_vector_store, store_embeddings


def index_document(
    document_id: str,
    parsed_text: str
):
    """
    Orchestrates STEP 2 → STEP 3 → STEP 4
    Chunking → Embedding → Vector Storage
    """

    # STEP 2: Chunking
    nodes = chunk_document(
        document_id=document_id,
        text=parsed_text,
        upload_timestamp=datetime.utcnow()
    )

    # STEP 3: Embedding
    embedded_nodes = generate_embeddings(nodes)

    # STEP 4: Vector Storage
    vector_store = get_vector_store()
    store_embeddings(embedded_nodes, vector_store)

    return len(embedded_nodes)
