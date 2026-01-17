const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

// ===========================
// CHAT STREAMING
// ===========================

export async function streamChat({ userId, sessionId, query }, onToken) {
  const response = await fetch(`${API_BASE}/chat/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_id: userId,
      session_id: sessionId,
      query: query,
    }),
  });

  if (!response.ok || !response.body) {
    const err = await response.text();
    throw new Error(err || "Chat request failed");
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder("utf-8");

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    onToken(decoder.decode(value));
  }
}

// ===========================
// SESSION MANAGEMENT
// ===========================

/**
 * Create a new chat session
 */
export async function createSession(userId, title = "New Chat") {
  const response = await fetch(`${API_BASE}/sessions/create`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_id: userId,
      title: title,
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to create session");
  }

  return await response.json();
}

/**
 * List all sessions for a user
 */
export async function listSessions(userId) {
  const response = await fetch(`${API_BASE}/sessions/list/${userId}`);

  if (!response.ok) {
    throw new Error("Failed to fetch sessions");
  }

  return await response.json();
}

/**
 * Get all messages for a specific session
 */
export async function getSessionMessages(sessionId) {
  const response = await fetch(
    `${API_BASE}/sessions/${sessionId}/messages`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch messages");
  }

  return await response.json();
}

/**
 * Update session title
 */
export async function updateSessionTitle(sessionId, title) {
  const response = await fetch(`${API_BASE}/sessions/${sessionId}/title`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title }),
  });

  if (!response.ok) {
    throw new Error("Failed to update title");
  }

  return await response.json();
}

/**
 * Delete a session
 */
export async function deleteSession(sessionId) {
  const response = await fetch(`${API_BASE}/sessions/${sessionId}`, {
    method: "DELETE",
  });

  if (!response.ok) {
    throw new Error("Failed to delete session");
  }

  return await response.json();
}

/**
 * Generate AI title from first message
 */
export async function generateSessionTitle(sessionId) {
  const response = await fetch(
    `${API_BASE}/sessions/${sessionId}/generate-title`,
    {
      method: "POST",
    }
  );

  if (!response.ok) {
    throw new Error("Failed to generate title");
  }

  return await response.json();
}