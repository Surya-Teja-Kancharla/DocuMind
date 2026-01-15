from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from backend.app.services.chat_session import (
    get_session_messages,
    append_session_message,
)
from backend.app.services.chat_history import store_chat_message
from backend.app.services.retriever import retrieve_similar_chunks
from backend.app.services.context_assembler import assemble_context
from backend.app.services.llm import stream_llm_response

router = APIRouter(prefix="/chat", tags=["Chat"])


# -----------------------------
# Request Schema
# -----------------------------
class ChatRequest(BaseModel):
    user_id: str
    session_id: str
    query: str


# -----------------------------
# Streaming Chat Endpoint
# -----------------------------
@router.post("/stream")
def chat_stream(payload: ChatRequest):
    """
    Streaming chat endpoint (Groq-backed).
    Fully typed + Swagger compatible.
    """

    # 1. Load recent session context (Redis)
    session_messages = get_session_messages(payload.session_id)

    # 2. Persist user message
    append_session_message(payload.session_id, "user", payload.query)
    store_chat_message(
        user_id=payload.user_id,
        session_id=payload.session_id,
        role="user",
        content=payload.query,
    )

    # 3. Retrieve document chunks
    retrieved_nodes = retrieve_similar_chunks(payload.query)

    # 4. Assemble RAG prompt
    prompt = assemble_context(
        user_query=payload.query,
        retrieved_nodes=retrieved_nodes,
        conversation_messages=session_messages,
    )

    # 5. Stream Groq response
    def token_stream():
        full_response = []

        for token in stream_llm_response(prompt):
            full_response.append(token)
            yield token

        final_answer = "".join(full_response)

        append_session_message(payload.session_id, "assistant", final_answer)
        store_chat_message(
            user_id=payload.user_id,
            session_id=payload.session_id,
            role="assistant",
            content=final_answer,
        )

    return StreamingResponse(token_stream(), media_type="text/plain")
