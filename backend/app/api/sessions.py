from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import logging
from datetime import datetime
import uuid  # ✅ ADDED FOR UUID GENERATION

from backend.app.core.config import get_supabase_client
from backend.app.services.llm import generate_answer

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/sessions", tags=["Session Management"])


# ===========================
# Request/Response Models
# ===========================

class CreateSessionRequest(BaseModel):
    user_id: str
    title: Optional[str] = "New Chat"


class UpdateSessionRequest(BaseModel):
    title: str


class SessionResponse(BaseModel):
    session_id: str
    user_id: str
    title: str
    created_at: str
    updated_at: str


class MessageResponse(BaseModel):
    role: str
    content: str
    created_at: str


# ===========================
# Session Management Endpoints
# ===========================

@router.post("/create", response_model=SessionResponse)
async def create_session(payload: CreateSessionRequest):
    """
    Create a new chat session for a user.
    ✅ FIXED: Now generates UUID in Python instead of relying on Supabase
    """
    client = get_supabase_client()
    if not client:
        raise HTTPException(status_code=503, detail="Database unavailable")

    try:
        # ✅ GENERATE UUID IN PYTHON
        session_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        
        # Insert with explicit session_id
        response = client.table("chat_sessions").insert({
            "session_id": session_id,  # ✅ EXPLICITLY PROVIDED
            "user_id": payload.user_id,
            "title": payload.title,
            "created_at": now,
            "updated_at": now
        }).execute()

        if not response.data:
            raise HTTPException(status_code=500, detail="Failed to create session")

        session = response.data[0]
        
        logger.info(f"Session created | session_id={session['session_id']} | user_id={payload.user_id}")
        
        return SessionResponse(
            session_id=session["session_id"],
            user_id=session["user_id"],
            title=session["title"],
            created_at=session["created_at"],
            updated_at=session["updated_at"]
        )

    except Exception as e:
        logger.error(f"Session creation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list/{user_id}", response_model=List[SessionResponse])
async def list_sessions(user_id: str):
    """
    Get all chat sessions for a user, ordered by most recent.
    """
    client = get_supabase_client()
    if not client:
        raise HTTPException(status_code=503, detail="Database unavailable")

    try:
        response = (
            client
            .table("chat_sessions")
            .select("*")
            .eq("user_id", user_id)
            .order("updated_at", desc=True)
            .execute()
        )

        sessions = [
            SessionResponse(
                session_id=s["session_id"],
                user_id=s["user_id"],
                title=s["title"],
                created_at=s["created_at"],
                updated_at=s["updated_at"]
            )
            for s in response.data
        ]

        logger.info(f"Sessions retrieved | user_id={user_id} | count={len(sessions)}")
        return sessions

    except Exception as e:
        logger.error(f"Session list failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{session_id}/messages", response_model=List[MessageResponse])
async def get_session_messages(session_id: str, limit: int = 50):
    """
    Get all messages for a specific session.
    """
    client = get_supabase_client()
    if not client:
        raise HTTPException(status_code=503, detail="Database unavailable")

    try:
        response = (
            client
            .table("chat_messages")
            .select("role, content, created_at")
            .eq("session_id", session_id)
            .order("created_at", desc=False)
            .limit(limit)
            .execute()
        )

        messages = [
            MessageResponse(
                role=m["role"],
                content=m["content"],
                created_at=m["created_at"]
            )
            for m in response.data
        ]

        logger.info(f"Messages retrieved | session_id={session_id} | count={len(messages)}")
        return messages

    except Exception as e:
        logger.error(f"Message retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{session_id}/title")
async def update_session_title(session_id: str, payload: UpdateSessionRequest):
    """
    Update the title of a session.
    Also updates the updated_at timestamp.
    """
    client = get_supabase_client()
    if not client:
        raise HTTPException(status_code=503, detail="Database unavailable")

    try:
        response = (
            client
            .table("chat_sessions")
            .update({
                "title": payload.title,
                "updated_at": datetime.utcnow().isoformat()
            })
            .eq("session_id", session_id)
            .execute()
        )

        if not response.data:
            raise HTTPException(status_code=404, detail="Session not found")

        logger.info(f"Session title updated | session_id={session_id} | title={payload.title}")
        
        return {"status": "success", "session_id": session_id, "title": payload.title}

    except Exception as e:
        logger.error(f"Title update failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{session_id}")
async def delete_session(session_id: str):
    """
    Delete a session and all its messages.
    """
    client = get_supabase_client()
    if not client:
        raise HTTPException(status_code=503, detail="Database unavailable")

    try:
        # Delete messages first (foreign key constraint)
        client.table("chat_messages").delete().eq("session_id", session_id).execute()
        
        # Delete session
        response = (
            client
            .table("chat_sessions")
            .delete()
            .eq("session_id", session_id)
            .execute()
        )

        logger.info(f"Session deleted | session_id={session_id}")
        
        return {"status": "success", "session_id": session_id}

    except Exception as e:
        logger.error(f"Session deletion failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===========================
# Auto-Title Generation
# ===========================

@router.post("/{session_id}/generate-title")
async def generate_session_title(session_id: str):
    """
    Generate a ChatGPT-like title from the first user message.
    """
    client = get_supabase_client()
    if not client:
        raise HTTPException(status_code=503, detail="Database unavailable")

    try:
        # Get first user message
        response = (
            client
            .table("chat_messages")
            .select("content")
            .eq("session_id", session_id)
            .eq("role", "user")
            .order("created_at", desc=False)
            .limit(1)
            .execute()
        )

        if not response.data:
            raise HTTPException(status_code=404, detail="No messages found")

        first_message = response.data[0]["content"]

        # Generate title using LLM
        title_prompt = f"""Generate a short, concise title (3-6 words) for a conversation that starts with:

"{first_message}"

Return ONLY the title, nothing else. No quotes, no punctuation at the end."""

        generated_title = generate_answer(title_prompt).strip().strip('"\'')
        
        # Limit to 50 characters
        if len(generated_title) > 50:
            generated_title = generated_title[:47] + "..."

        # Update session title
        client.table("chat_sessions").update({
            "title": generated_title,
            "updated_at": datetime.utcnow().isoformat()
        }).eq("session_id", session_id).execute()

        logger.info(f"Title generated | session_id={session_id} | title={generated_title}")

        return {"status": "success", "session_id": session_id, "title": generated_title}

    except Exception as e:
        logger.error(f"Title generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))