from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from backend.app.services.chat_session import (
    get_session_messages,
    append_session_message
)
from backend.app.services.chat_history import store_chat_message
from backend.app.services.retriever import retrieve_similar_chunks

router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatRequest(BaseModel):
    user_id: str
    session_id: str
    query: str


class RetrievedChunk(BaseModel):
    text: str
    metadata: dict


@router.post("/")
def chat_entrypoint(payload: ChatRequest):

    # 1. Load session context
    session_context = get_session_messages(payload.session_id)

    # 2. Store user message
    append_session_message(payload.session_id, payload.query)
    store_chat_message(
        user_id=payload.user_id,
        session_id=payload.session_id,
        role="user",
        content=payload.query
    )

    # 3. Retrieve relevant document chunks
    retrieved_nodes = retrieve_similar_chunks(payload.query)

    retrieved_chunks = [
        RetrievedChunk(
            text=node.text,
            metadata=node.metadata
        )
        for node in retrieved_nodes
    ]

    # 4. (LLM answer generation intentionally deferred)

    return {
        "session_context": session_context,
        "retrieved_chunks": retrieved_chunks,
        "message": "Retrieval successful (answer generation pending)"
    }
