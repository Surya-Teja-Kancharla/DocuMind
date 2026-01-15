const API_BASE = import.meta.env.VITE_API_BASE;

export async function streamChat({ sessionId, message, onToken }) {
  const response = await fetch(`${API_BASE}/chat/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      session_id: sessionId,
      message
    })
  });

  if (!response.body) {
    throw new Error("Streaming not supported");
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder("utf-8");

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    onToken(decoder.decode(value));
  }
}
