import { useEffect, useRef, useState } from "react";
import Message from "./Message";
import WelcomePanel from "./WelcomePanel";
import ChatInput from "./ChatInput";
import { streamChat } from "../api/chat";
import { uploadDocumentWithProgress } from "../api/upload";

const USER_ID = "local-user"; // TODO: replace with auth later

const ChatWindow = ({ session, onUpdateSession }) => {
  const [input, setInput] = useState("");

  // Upload state
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [documentReady, setDocumentReady] = useState(false);

  const bottomRef = useRef(null);

  const isEmptyConversation =
    session.messages.length === 1 &&
    session.messages[0].role === "assistant";

  // Auto-scroll on new messages
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [session.messages]);

  // -----------------------------
  // Document Upload Handler
  // -----------------------------
  const handleUpload = async (e) => {
    const selectedFiles = Array.from(e.target.files);
    if (!selectedFiles.length) return;

    setFiles(selectedFiles);
    setUploading(true);
    setUploadProgress(0);
    setDocumentReady(false);

    try {
      for (let i = 0; i < selectedFiles.length; i++) {
        await uploadDocumentWithProgress({
          file: selectedFiles[i],
          userId: USER_ID,
          sessionId: session.id,
          onProgress: (p) => {
            const overall =
              Math.round(
                (i / selectedFiles.length) * 100 +
                  p / selectedFiles.length
              );
            setUploadProgress(overall);
          },
        });
      }

      setDocumentReady(true);
    } catch (err) {
      console.error("Upload failed", err);
      setFiles([]);
      setDocumentReady(false);
    } finally {
      setUploading(false);
    }
  };

  // -----------------------------
  // Send Message (Streaming)
  // -----------------------------
  const sendMessage = async () => {
    // Block sending while upload is in progress or ingestion not finished
    if (!input.trim() || uploading || !documentReady) return;

    const userMsg = { role: "user", content: input };
    const assistantMsg = {
      role: "assistant",
      content: "",
      isStreaming: true,
    };

    const updatedMessages = [
      ...session.messages,
      userMsg,
      assistantMsg,
    ];

    onUpdateSession({ ...session, messages: updatedMessages });

    const assistantIndex = updatedMessages.length - 1;
    setInput("");

    let buffer = "";
    let typing = false;

    const typeWriter = async () => {
      if (typing) return;
      typing = true;

      while (buffer.length > 0) {
        const char = buffer[0];
        buffer = buffer.slice(1);

        onUpdateSession((prev) => {
          const msgs = [...prev.messages];
          msgs[assistantIndex] = {
            ...msgs[assistantIndex],
            content: msgs[assistantIndex].content + char,
          };
          return { ...prev, messages: msgs };
        });

        await new Promise((r) => setTimeout(r, 15));
      }

      typing = false;
    };

    try {
      await streamChat(
        {
          userId: USER_ID,
          sessionId: session.id,
          query: userMsg.content,
        },
        (chunk) => {
          buffer += chunk;
          typeWriter();
        }
      );

      onUpdateSession((prev) => {
        const msgs = [...prev.messages];
        msgs[assistantIndex].isStreaming = false;
        return { ...prev, messages: msgs };
      });
    } catch (err) {
      console.error("Chat streaming failed", err);

      onUpdateSession((prev) => {
        const msgs = [...prev.messages];
        msgs[assistantIndex] = {
          role: "assistant",
          content:
            "⚠️ An error occurred while generating the response.",
          isStreaming: false,
        };
        return { ...prev, messages: msgs };
      });
    }
  };

  return (
    <div className="flex flex-col h-full w-full bg-slate-900">
      {/* Welcome / Empty State */}
      {isEmptyConversation ? (
        <WelcomePanel />
      ) : (
        <div className="flex-1 overflow-y-auto px-6 py-4">
          {session.messages.map((msg, idx) => (
            <Message key={idx} {...msg} />
          ))}
          <div ref={bottomRef} />
        </div>
      )}

      {/* Upload Progress */}
      {uploading && (
        <div className="w-full max-w-3xl mx-auto mb-2 px-4">
          <div className="bg-slate-700 h-1 rounded overflow-hidden">
            <div
              className="bg-blue-600 h-full transition-all duration-300"
              style={{ width: `${uploadProgress}%` }}
            />
          </div>
          <p className="text-[10px] text-slate-500 mt-1 text-center uppercase tracking-widest">
            Indexing documents… {uploadProgress}%
          </p>
        </div>
      )}

      {/* Chat Input Area */}
      <div className="flex justify-center px-4 py-8">
        <div className="w-full max-w-3xl">
          <ChatInput
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onSend={sendMessage}
            disabled={uploading || !documentReady}
            attachments={files}
            onUpload={handleUpload}
            onRemove={(i) => {
              setFiles((prev) =>
                prev.filter((_, idx) => idx !== i)
              );
              setDocumentReady(false);
            }}
          />
        </div>
      </div>
    </div>
  );
};

export default ChatWindow;
