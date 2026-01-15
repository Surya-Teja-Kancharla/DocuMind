import React from "react";

const Sidebar = ({
  sessions = [],
  activeSessionId,
  onSelectSession = () => {},
  onNewChat = () => {},
  open = false,
  toggle = () => {}
}) => {
  return (
    <>
      {/* HAMBURGER TOGGLE */}
      {!open && (
        <button
          onClick={(e) => {
            e.stopPropagation();
            toggle();
          }}
          className="fixed top-4 left-4 z-[60] 
                     bg-slate-900 text-white 
                     p-2 rounded-md shadow-lg
                     hover:bg-slate-800 transition-colors"
          title="Open sidebar"
        >
          ☰
        </button>
      )}

      {/* SIDEBAR OVERLAY */}
      {open && (
        <div 
          className="fixed inset-0 bg-black/20 z-40 md:hidden" 
          onClick={toggle}
        />
      )}

      {/* SIDEBAR CONTAINER */}
      <div
        className={`
          fixed top-0 left-0 h-full
          z-50 
          transition-all duration-300 ease-in-out
          ${open ? "w-64" : "w-0"}
          bg-slate-900 text-white
          overflow-hidden
          flex flex-col
          border-r border-slate-700
        `}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-slate-700 min-w-[256px]">
          <span className="font-bold text-xl tracking-tight text-blue-400">DocuMind</span>
          <button
            onClick={toggle}
            className="p-2 rounded-full hover:bg-slate-800 text-slate-400 hover:text-white"
            title="Close sidebar"
          >
            ✕
          </button>
        </div>

        {/* Sessions List */}
        <div className="flex-1 overflow-y-auto p-3 space-y-2 min-w-[256px]">
          <p className="text-xs font-semibold text-slate-500 uppercase px-2 pb-1">Recent Chats</p>
          {sessions.length === 0 ? (
            <p className="text-sm text-slate-500 px-2 italic">No sessions yet</p>
          ) : (
            sessions.map((s) => (
              <div
                key={s.id}
                onClick={() => onSelectSession(s.id)}
                className={`px-3 py-2.5 rounded-lg cursor-pointer text-sm transition-all
                  ${
                    s.id === activeSessionId
                      ? "bg-slate-800 text-blue-400 border border-slate-700"
                      : "text-slate-300 hover:bg-slate-800 hover:text-white"
                  }`}
              >
                <div className="truncate w-full">{s.title || "Untitled Chat"}</div>
              </div>
            ))
          )}
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-slate-700 min-w-[256px]">
          <button
            onClick={() => {
              onNewChat();
              if (window.innerWidth < 768) toggle();
            }}
            className="w-full bg-blue-600 hover:bg-blue-500 text-white font-medium py-2.5 rounded-lg transition-colors shadow-md"
          >
            + New Chat
          </button>
        </div>
      </div>
    </>
  );
};

export default Sidebar;