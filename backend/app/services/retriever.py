from llama_index.core import VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from backend.app.services.vector_store import get_vector_store


def retrieve_similar_chunks(
    query: str,
    top_k: int = 5
):
    """
    Retrieve top-k semantically similar chunks from Milvus.
    """

    embed_model = HuggingFaceEmbedding(
        model_name="nomic-ai/nomic-embed-text-v1.5",
        trust_remote_code=True
    )

    vector_store = get_vector_store()

    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        embed_model=embed_model  # ✅ CRITICAL FIX
    )

    retriever = index.as_retriever(similarity_top_k=top_k)

    return retriever.retrieve(query)
