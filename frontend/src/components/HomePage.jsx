import { useState } from "react";
import Sidebar from "../components/Sidebar";
import ChatWindow from "../components/ChatWindow";
import { v4 as uuid } from "uuid";

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
  const [activeSessionId, setActiveSessionId] = useState(sessions[0].id);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const activeSession = sessions.find((s) => s.id === activeSessionId);

  const updateSession = (updated) => {
    setSessions((prev) =>
      prev.map((s) =>
        s.id === activeSessionId
          ? typeof updated === "function"
            ? updated(s)
            : updated
          : s
      )
    );
  };

  const newChat = () => {
    const session = createSession();
    setSessions((prev) => [session, ...prev]);
    setActiveSessionId(session.id);
    if (window.innerWidth < 768) setIsSidebarOpen(false);
  };

  const toggleSidebar = () => {
    setIsSidebarOpen((prev) => !prev);
  };

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-slate-50">
      <Sidebar
        sessions={sessions}
        activeSessionId={activeSessionId}
        onSelectSession={(id) => {
            setActiveSessionId(id);
            if (window.innerWidth < 768) setIsSidebarOpen(false);
        }}
        onNewChat={newChat}
        open={isSidebarOpen}
        toggle={toggleSidebar}
      />
      
      <div 
        className={`flex-1 flex flex-col transition-all duration-300 ease-in-out ${
          isSidebarOpen ? "ml-64" : "ml-0"
        }`}
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