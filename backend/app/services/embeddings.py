from typing import List

from llama_index.core.schema import TextNode
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


def generate_embeddings(
    nodes: List[TextNode],
    model_name: str = "nomic-ai/nomic-embed-text-v1.5"
):
    """
    Generate embeddings for chunked TextNodes.

    Returns:
    - nodes with embeddings populated
    """

    embed_model = HuggingFaceEmbedding(
        model_name=model_name,
        trust_remote_code=True
    )

    for node in nodes:
        node.embedding = embed_model.get_text_embedding(node.text)

    return nodes
