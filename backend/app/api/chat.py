from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import logging

from backend.app.services.chat_session import (
    get_session_messages,
    append_session_message,
)
from backend.app.services.chat_history import store_chat_message
from backend.app.services.retriever import retrieve_similar_chunks
from backend.app.services.context_assembler import assemble_context
from backend.app.services.llm import stream_llm_response

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatRequest(BaseModel):
    user_id: str
    session_id: str
    query: str


@router.post("/stream")
async def chat_stream(payload: ChatRequest):
    """
    Streaming RAG chat endpoint with deterministic error signaling.
    """

    # 1. Persist user message first
    append_session_message(payload.session_id, "user", payload.query)
    store_chat_message(
        user_id=payload.user_id,
        session_id=payload.session_id,
        role="user",
        content=payload.query,
    )

    # 2. Load session context
    session_messages = get_session_messages(payload.session_id)

    # 3. Retrieve document chunks
    retrieved_nodes = retrieve_similar_chunks(
        payload.query,
        session_id=payload.session_id
    )

    # 4. Assemble prompt
    prompt = assemble_context(
        user_query=payload.query,
        retrieved_nodes=retrieved_nodes,
        conversation_messages=session_messages,
    )

    # 5. Streaming generator with hard error guarantees
    async def token_stream():
        full_response = []

        try:
            async for token in stream_llm_response(prompt):
                full_response.append(token)
                yield token

        except Exception as e:
            logger.error(f"Streaming failed: {e}")
            yield "\n\n⚠️ The response was interrupted. Please retry."
            return

        # Persist assistant response only if stream completed
        final_answer = "".join(full_response)

        append_session_message(payload.session_id, "assistant", final_answer)
        store_chat_message(
            user_id=payload.user_id,
            session_id=payload.session_id,
            role="assistant",
            content=final_answer,
        )

    return StreamingResponse(
        token_stream(),
        media_type="text/plain"
    )
