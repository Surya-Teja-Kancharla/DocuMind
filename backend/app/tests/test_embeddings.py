from datetime import datetime
from pathlib import Path

from backend.app.services.chunking import chunk_document
from backend.app.services.embeddings import generate_embeddings


PARSED_DIR = Path("data/parsed")
parsed_file = list(PARSED_DIR.glob("*.txt"))[0]

parsed_text = parsed_file.read_text(encoding="utf-8")
document_id = parsed_file.stem

nodes = chunk_document(
    document_id=document_id,
    text=parsed_text,
    upload_timestamp=datetime.utcnow()
)

embedded_nodes = generate_embeddings(nodes)

print(f"Total nodes: {len(embedded_nodes)}")
print(f"Embedding dimension: {len(embedded_nodes[0].embedding)}")
print(f"Sample embedding (first 5 values): {embedded_nodes[0].embedding[:5]}")
