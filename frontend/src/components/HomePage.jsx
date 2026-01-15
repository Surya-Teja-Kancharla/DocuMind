import { useState } from "react";
import Sidebar from "./Sidebar";
import ChatWindow from "./ChatWindow";
import { v4 as uuid } from "uuid";

const SIDEBAR_WIDTH = 256; // matches w-64

const createSession = () => ({
  id: uuid(),
  title: "New Chat",
  messages: [
    {
      role: "assistant",
      content: "Hello! Upload a document and ask me questions about it.",
    },
  ],
});

const HomePage = () => {
  const [sessions, setSessions] = useState([createSession()]);
  const [activeId, setActiveId] = useState(sessions[0].id);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const activeSession = sessions.find((s) => s.id === activeId);

  const updateSession = (updater) => {
    setSessions((prev) =>
      prev.map((s) =>
        s.id === activeId
          ? typeof updater === "function"
            ? updater(s)
            : updater
          : s
      )
    );
  };

  const newChat = () => {
    const s = createSession();
    setSessions((prev) => [s, ...prev]);
    setActiveId(s.id);
    setSidebarOpen(false);
  };

  const deleteSession = (id) => {
    setSessions((prev) => {
      const remaining = prev.filter((s) => s.id !== id);
      if (id === activeId && remaining.length > 0) {
        setActiveId(remaining[0].id);
      }
      return remaining.length ? remaining : [createSession()];
    });
  };

  return (
    <div className="h-screen w-screen overflow-hidden bg-slate-950">
      {/* FIXED SIDEBAR */}
      <Sidebar
        sessions={sessions}
        activeSessionId={activeId}
        onSelectSession={(id) => {
          setActiveId(id);
          setSidebarOpen(false);
        }}
        onNewChat={newChat}
        onDeleteSession={deleteSession}
        open={sidebarOpen}
        toggle={() => setSidebarOpen((o) => !o)}
      />

      {/* MAIN CONTENT — PUSHED BY SIDEBAR */}
      <div
        className="h-full transition-all duration-300 ease-in-out"
        style={{
          marginLeft: sidebarOpen ? SIDEBAR_WIDTH : 0,
        }}
      >
        <ChatWindow
          session={activeSession}
          onUpdateSession={updateSession}
        />
      </div>
    </div>
  );
};

export default HomePage;
