from datetime import datetime
from typing import List

from llama_index.core import Document
from llama_index.core.schema import TextNode
from llama_index.core.node_parser import SentenceSplitter


def chunk_document(
    document_id: str,
    text: str,
    upload_timestamp: datetime,
    chunk_size: int = 512,
    chunk_overlap: int = 100
) -> List[TextNode]:
    """
    Split document text into context-preserving chunks
    and enrich each chunk with metadata.
    """

    # Step 1: Wrap raw text into a LlamaIndex Document
    document = Document(
        text=text,
        metadata={
            "document_id": document_id,
            "upload_timestamp": upload_timestamp.isoformat()
        }
    )

    # Step 2: Initialize the NodeParser
    parser = SentenceSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    # Step 3: Generate nodes (chunks)
    nodes = parser.get_nodes_from_documents([document])

    # Step 4: Enrich metadata per chunk
    for idx, node in enumerate(nodes):
        node.metadata.update({
            "chunk_id": f"{document_id}_chunk_{idx}",
            "chunk_index": idx,
            "page_number": None,   # placeholder
            "section": None        # placeholder
        })

    return nodes
