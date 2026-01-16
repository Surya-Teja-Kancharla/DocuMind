from llama_index.core import VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.vector_stores import MetadataFilters, ExactMatchFilter

from backend.app.services.vector_store import get_vector_store


def retrieve_similar_chunks(
    query: str,
    session_id: str,
    top_k: int = 5
):
    """
    Retrieve top-k semantically similar chunks
    scoped strictly to the given session_id.
    """

    embed_model = HuggingFaceEmbedding(
        model_name="nomic-ai/nomic-embed-text-v1.5",
        trust_remote_code=True
    )

    vector_store = get_vector_store()

    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        embed_model=embed_model
    )

    # ✅ CORRECT FILTER OBJECT
    filters = MetadataFilters(
        filters=[
            ExactMatchFilter(
                key="session_id",
                value=session_id
            )
        ]
    )

    retriever = index.as_retriever(
        similarity_top_k=top_k,
        filters=filters
    )

    return retriever.retrieve(query)
    