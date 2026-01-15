import { useEffect, useRef, useState } from "react";
import Message from "./Message";
import WelcomePanel from "./WelcomePanel";
import ChatInput from "./ChatInput";
import { streamChat } from "../api/chat";

const ChatWindow = ({ session, onUpdateSession }) => {
  const [input, setInput] = useState("");
  const [documentReady, setDocumentReady] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const bottomRef = useRef(null);

  const isEmptyConversation =
    session.messages.length === 1 &&
    session.messages[0].role === "assistant";

  // Auto-scroll
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [session.messages]);

  const sendMessage = async () => {
    if (!input.trim() || !documentReady) return;

    const userMsg = { role: "user", content: input };
    const assistantMsg = { role: "assistant", content: "", isStreaming: true };

    const messages = [...session.messages, userMsg, assistantMsg];
    onUpdateSession({ ...session, messages });

    const assistantIndex = messages.length - 1;
    setInput("");

    let buffer = "";
    let typing = false;

    const typeWriter = async () => {
      if (typing) return;
      typing = true;

      while (buffer.length > 0) {
        const char = buffer[0];
        buffer = buffer.slice(1);

        onUpdateSession(prev => {
          const msgs = [...prev.messages];
          msgs[assistantIndex].content += char;
          return { ...prev, messages: msgs };
        });

        await new Promise(r => setTimeout(r, 15));
      }

      typing = false;
    };

    try {
      await streamChat({
        sessionId: session.id,
        message: userMsg.content,
        onToken: chunk => {
          buffer += chunk;
          typeWriter();
        }
      });

      onUpdateSession(prev => {
        const msgs = [...prev.messages];
        msgs[assistantIndex].isStreaming = false;
        return { ...prev, messages: msgs };
      });
    } catch (err) {
      onUpdateSession(prev => {
        const msgs = [...prev.messages];
        msgs[assistantIndex].content =
          "⚠️ An error occurred while generating the response.";
        msgs[assistantIndex].isStreaming = false;
        return { ...prev, messages: msgs };
      });
    }
  };

  return (
    <div className="flex flex-col h-full w-full bg-gradient-to-b from-slate-900 to-blue-900">
      
      {/* Empty / Welcome State */}
      {isEmptyConversation ? (
        <WelcomePanel
          input={input}
          setInput={setInput}
          sendMessage={sendMessage}
          documentReady={documentReady}
        />
      ) : (
        <div className="flex-1 overflow-y-auto px-6 py-4">
          {session.messages.map((msg, idx) => (
            <Message key={idx} {...msg} />
          ))}
          <div ref={bottomRef} />
        </div>
      )}

      {/* Upload progress (optional) */}
      {uploadProgress > 0 && uploadProgress < 100 && (
        <div className="w-full max-w-3xl mx-auto mb-2 bg-slate-700 h-1 rounded">
          <div
            className="bg-blue-600 h-full transition-all"
            style={{ width: `${uploadProgress}%` }}
          />
        </div>
      )}

      {/* ChatGPT-style input */}
      <div className="flex justify-center px-4 py-6">
        <ChatInput
          input={input}
          setInput={setInput}
          sendMessage={sendMessage}
          documentReady={documentReady}
          setDocumentReady={setDocumentReady}
          setUploadProgress={setUploadProgress}
          uploading={uploadProgress > 0 && uploadProgress < 100}
        />
      </div>
    </div>
  );
};

export default ChatWindow;
