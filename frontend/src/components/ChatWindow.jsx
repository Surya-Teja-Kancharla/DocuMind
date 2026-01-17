import { useEffect, useRef, useState } from "react";
import Message from "./Message";
import WelcomePanel from "./WelcomePanel";
import ChatInput from "./ChatInput";
import { streamChat, generateSessionTitle } from "../api/chat";
import { uploadDocumentWithProgress } from "../api/upload";

const USER_ID = "local-user";

const ChatWindow = ({ session, onUpdateSession }) => {
  const [input, setInput] = useState("");
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [documentReady, setDocumentReady] = useState(false);
  const [showToast, setShowToast] = useState(false);
  const [toastMessage, setToastMessage] = useState("");

  const containerRef = useRef(null);
  const bottomRef = useRef(null);
  const titleGeneratedRef = useRef(false);

  const isEmptyConversation = session.messages.length === 0;

  // Smart auto-scroll
  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;

    const nearBottom =
      el.scrollHeight - el.scrollTop - el.clientHeight < 120;

    if (nearBottom) {
      bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [session.messages]);

  // Toast notifications
  useEffect(() => {
    if (documentReady) {
      showToastNotification("Document indexed successfully");
    }
  }, [documentReady]);

  const showToastNotification = (message) => {
    setToastMessage(message);
    setShowToast(true);
    const t = setTimeout(() => setShowToast(false), 2000);
    return () => clearTimeout(t);
  };

  // Reset title generation flag when session changes
  useEffect(() => {
    titleGeneratedRef.current = false;
  }, [session.id]);

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
            const overall = Math.round(
              (i / selectedFiles.length) * 100 + p / selectedFiles.length
            );
            setUploadProgress(overall);
          },
        });
      }
      setDocumentReady(true);
    } catch (error) {
      console.error("Upload failed:", error);
      setFiles([]);
      showToastNotification("Upload failed. Please try again.");
    } finally {
      setUploading(false);
    }
  };

  const sendMessage = async () => {
    if (!input.trim() || uploading) return;

    // ✅ Optional: Warn if no document uploaded yet
    if (!documentReady && session.messages.length === 0) {
      showToastNotification("💡 Tip: Upload a document for context-aware answers");
      await new Promise((r) => setTimeout(r, 1500));
    }

    const userMsg = { role: "user", content: input };
    const assistantMsg = {
      role: "assistant",
      content: "",
      isStreaming: true,
    };

    const updatedMessages = [...session.messages, userMsg, assistantMsg];

    onUpdateSession({ ...session, messages: updatedMessages });
    setInput("");

    const assistantIndex = updatedMessages.length - 1;

    // ✅ FIXED: Direct streaming without typewriter effect
    // Avoids duplication issues with buffer/typing state
    let fullResponse = "";

    try {
      await streamChat(
        {
          userId: USER_ID,
          sessionId: session.id,
          query: userMsg.content,
        },
        (chunk) => {
          // ✅ FIXED: Accumulate and update directly
          fullResponse += chunk;
          
          // Update message content immediately
          onUpdateSession((prev) => {
            const msgs = [...prev.messages];
            if (msgs[assistantIndex]) {
              msgs[assistantIndex] = {
                ...msgs[assistantIndex],
                content: fullResponse,
                isStreaming: true
              };
            }
            return { ...prev, messages: msgs };
          });
        }
      );

      // Mark streaming as complete
      onUpdateSession((prev) => {
        const msgs = [...prev.messages];
        if (msgs[assistantIndex]) {
          msgs[assistantIndex].isStreaming = false;
        }
        return { ...prev, messages: msgs };
      });

      // ✅ AUTO-GENERATE TITLE AFTER FIRST MESSAGE
      if (
        !titleGeneratedRef.current &&
        session.messages.length === 0 &&
        session.title === "New Chat"
      ) {
        titleGeneratedRef.current = true;
        try {
          const result = await generateSessionTitle(session.id);
          onUpdateSession((prev) => ({
            ...prev,
            title: result.title,
          }));
        } catch (error) {
          console.error("Title generation failed:", error);
        }
      }
    } catch (error) {
      console.error("Chat failed:", error);
      onUpdateSession((prev) => {
        const msgs = [...prev.messages];
        msgs[assistantIndex] = {
          role: "assistant",
          content: "⚠️ An error occurred while generating the response.",
          isStreaming: false,
        };
        return { ...prev, messages: msgs };
      });
    }
  };

  return (
    <div className="flex flex-col h-full w-full bg-slate-900 relative">
      {/* TOAST NOTIFICATION */}
      {showToast && (
        <div className="absolute top-4 right-4 bg-green-600 text-white text-sm px-4 py-2 rounded-lg shadow-lg z-50 animate-slide-in">
          {toastMessage}
        </div>
      )}

      {/* MAIN CONTENT */}
      {isEmptyConversation ? (
        <WelcomePanel />
      ) : (
        <div ref={containerRef} className="flex-1 overflow-y-auto px-6 py-4">
          {session.messages.map((msg, idx) => (
            <Message key={idx} {...msg} />
          ))}
          <div ref={bottomRef} />
        </div>
      )}

      {/* UPLOAD PROGRESS BAR */}
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

      {/* CHAT INPUT */}
      <div className="flex justify-center px-4 py-8">
        <ChatInput
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onSend={sendMessage}
          disabled={uploading}
          attachments={files}
          onUpload={handleUpload}
          onRemove={(i) => {
            setFiles((prev) => prev.filter((_, idx) => idx !== i));
            setDocumentReady(false);
          }}
        />
      </div>
    </div>
  );
};

export default ChatWindow;