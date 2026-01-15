const API_BASE = import.meta.env.VITE_API_BASE;

export async function streamChat(
  { userId, sessionId, query },
  onToken
) {
  const response = await fetch(`${API_BASE}/chat/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_id: userId,        // ✅ REQUIRED
      session_id: sessionId,  // ✅ REQUIRED
      query: query            // ✅ REQUIRED
    })
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
