from datetime import datetime
from pathlib import Path

from backend.app.services.chunking import chunk_document
from backend.app.services.embeddings import generate_embeddings
from backend.app.services.vector_store import get_vector_store, store_embeddings

PARSED_DIR = Path("data/parsed")
parsed_file = list(PARSED_DIR.glob("*.txt"))[0]

parsed_text = parsed_file.read_text(encoding="utf-8")
document_id = parsed_file.stem

# Chunk
nodes = chunk_document(
    document_id=document_id,
    text=parsed_text,
    upload_timestamp=datetime.utcnow()
)

# Embed
embedded_nodes = generate_embeddings(nodes)

# Store
vector_store = get_vector_store()
store_embeddings(embedded_nodes, vector_store)

print(f"Stored {len(embedded_nodes)} vectors in Milvus.")
