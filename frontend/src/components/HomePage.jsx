import { useState, useEffect } from "react";
import Sidebar from "./Sidebar";
import ChatWindow from "./ChatWindow";
import {
  createSession,
  listSessions,
  getSessionMessages,
  deleteSession as deleteSessionAPI,
} from "../api/chat";

const SIDEBAR_WIDTH = 256; // matches w-64
const USER_ID = "local-user"; // In production, this would come from auth

const HomePage = () => {
  const [sessions, setSessions] = useState([]);
  const [activeId, setActiveId] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [loading, setLoading] = useState(true);

  // ===========================
  // LOAD SESSIONS ON STARTUP
  // ===========================
  useEffect(() => {
    loadUserSessions();
  }, []);

  const loadUserSessions = async () => {
    try {
      setLoading(true);
      const backendSessions = await listSessions(USER_ID);

      if (backendSessions.length === 0) {
        // No sessions exist - create first one
        await createNewSession();
      } else {
        // Load existing sessions
        const sessionsWithMessages = await Promise.all(
          backendSessions.map(async (s) => {
            try {
              const messages = await getSessionMessages(s.session_id);
              return {
                id: s.session_id,
                title: s.title,
                messages: messages.map((m) => ({
                  role: m.role,
                  content: m.content,
                })),
                created_at: s.created_at,
                updated_at: s.updated_at,
              };
            } catch (error) {
              console.error(
                `Failed to load messages for session ${s.session_id}:`,
                error
              );
              return {
                id: s.session_id,
                title: s.title,
                messages: [],
                created_at: s.created_at,
                updated_at: s.updated_at,
              };
            }
          })
        );

        setSessions(sessionsWithMessages);
        setActiveId(sessionsWithMessages[0].id);
      }
    } catch (error) {
      console.error("Failed to load sessions:", error);
      // Fallback: create a new session
      await createNewSession();
    } finally {
      setLoading(false);
    }
  };

  // ===========================
  // SESSION OPERATIONS
  // ===========================

  const createNewSession = async () => {
    try {
      const newSession = await createSession(USER_ID, "New Chat");

      const sessionObj = {
        id: newSession.session_id,
        title: newSession.title,
        messages: [],
        created_at: newSession.created_at,
        updated_at: newSession.updated_at,
      };

      setSessions((prev) => [sessionObj, ...prev]);
      setActiveId(sessionObj.id);
      setSidebarOpen(false);
    } catch (error) {
      console.error("Failed to create session:", error);
      alert("Failed to create new chat. Please try again.");
    }
  };

  const deleteSessionHandler = async (id) => {
    try {
      await deleteSessionAPI(id);

      setSessions((prev) => {
        const remaining = prev.filter((s) => s.id !== id);

        // If deleting active session, switch to another
        if (id === activeId && remaining.length > 0) {
          setActiveId(remaining[0].id);
        } else if (remaining.length === 0) {
          // No sessions left - create a new one
          createNewSession();
        }

        return remaining;
      });
    } catch (error) {
      console.error("Failed to delete session:", error);
      alert("Failed to delete chat. Please try again.");
    }
  };

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

  // ===========================
  // RENDER
  // ===========================

  const activeSession = sessions.find((s) => s.id === activeId);

  if (loading) {
    return (
      <div className="h-screen w-screen flex items-center justify-center bg-slate-950 text-white">
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-slate-400">Loading your chats...</p>
        </div>
      </div>
    );
  }

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
        onNewChat={createNewSession}
        onDeleteSession={deleteSessionHandler}
        open={sidebarOpen}
        toggle={() => setSidebarOpen((o) => !o)}
      />

      {/* MAIN CONTENT – PUSHED BY SIDEBAR */}
      <div
        className="h-full transition-all duration-300 ease-in-out"
        style={{
          marginLeft: sidebarOpen ? SIDEBAR_WIDTH : 0,
        }}
      >
        {activeSession ? (
          <ChatWindow
            session={activeSession}
            onUpdateSession={updateSession}
          />
        ) : (
          <div className="h-full flex items-center justify-center text-white">
            <div className="text-center">
              <h2 className="text-2xl font-bold mb-4">No Active Session</h2>
              <button
                onClick={createNewSession}
                className="px-6 py-3 bg-blue-600 rounded-lg hover:bg-blue-500"
              >
                Create New Chat
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default HomePage;