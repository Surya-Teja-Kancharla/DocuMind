from typing import List

from llama_index.core.schema import TextNode
from llama_index.vector_stores.milvus import MilvusVectorStore
from llama_index.core import StorageContext


def get_vector_store(
    collection_name: str = "documind_documents",
    dim: int = 768
) -> MilvusVectorStore:
    """
    Initialize Milvus vector store.
    """

    vector_store = MilvusVectorStore(
        uri="tcp://localhost:19530",   # REQUIRED
        collection_name=collection_name,
        dim=dim,
        overwrite=False  # do NOT delete existing collections
    )

    return vector_store


def store_embeddings(
    nodes: List[TextNode],
    vector_store: MilvusVectorStore
):
    """
    Persist embedded nodes into Milvus.
    """

    storage_context = StorageContext.from_defaults(
        vector_store=vector_store
    )

    vector_store.add(nodes)

    return storage_context
