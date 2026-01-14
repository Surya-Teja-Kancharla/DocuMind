from typing import List
from llama_index.core import VectorStoreIndex
from llama_index.core.schema import TextNode
from backend.app.services.vector_store import get_vector_store


def retrieve_similar_chunks(
    query: str,
    top_k: int = 5
) -> List[TextNode]:

    vector_store = get_vector_store()

    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store
    )

    retriever = index.as_retriever(
        similarity_top_k=top_k
    )

    return retriever.retrieve(query)
