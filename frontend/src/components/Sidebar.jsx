const Sidebar = ({
  sessions = [],
  activeSessionId,
  onSelectSession = () => {},
  onNewChat = () => {},
  onDeleteSession = () => {},
  open = false,
  toggle = () => {},
}) => {
  return (
    <>
      {/* Hamburger when closed */}
      {!open && (
        <button
          onClick={toggle}
          className="fixed top-4 left-4 z-[60] bg-slate-900 text-white p-2 rounded-md hover:bg-slate-800 transition-colors shadow-lg"
          title="Open sidebar"
        >
          ☰
        </button>
      )}

      {/* Overlay on mobile */}
      {open && (
        <div
          className="fixed inset-0 bg-black/40 z-40 md:hidden backdrop-blur-sm"
          onClick={toggle}
        />
      )}

      {/* Sidebar Container */}
      <div
        className={`fixed top-0 left-0 h-full z-50 bg-slate-900 text-white
          transition-all duration-300 ease-in-out overflow-hidden flex flex-col border-r border-slate-700
          ${open ? "w-64 shadow-2xl" : "w-0"}`}
      >
        {/* Header */}
        <div className="flex justify-between items-center p-4 border-b border-slate-700 min-w-[256px]">
          <span className="text-xl font-bold text-blue-400 tracking-tight">DocuMind</span>
          <button 
            onClick={toggle} 
            className="p-1 hover:bg-slate-800 rounded text-slate-400 hover:text-red-400 transition-colors"
          >
            ✕
          </button>
        </div>

        {/* Sessions List */}
        <div className="flex-1 overflow-y-auto p-3 space-y-1 min-w-[256px]">
          <p className="text-[10px] font-bold text-slate-500 uppercase px-2 mb-2 tracking-wider">
            Recent Chats
          </p>

          {sessions.map((s) => (
            <div
              key={s.id}
              onClick={() => onSelectSession(s.id)}
              /* FIXED: Changed to a template literal backtick string */
              className={`group flex justify-between items-center px-3 py-2.5 rounded-lg cursor-pointer
                text-sm transition-all duration-200
                ${s.id === activeSessionId 
                  ? "bg-slate-800 text-blue-400 border border-slate-700" 
                  : "text-slate-300 hover:bg-slate-800 hover:text-white"
                }`}
            >
              <span className="truncate pr-2 font-medium">{s.title || "Untitled Chat"}</span>

              <button
                onClick={(e) => {
                  e.stopPropagation();
                  onDeleteSession(s.id);
                }}
                className="opacity-0 group-hover:opacity-100 p-1 hover:bg-slate-700 rounded transition-all text-slate-500 hover:text-red-400"
                title="Delete chat"
              >
                <span className="text-xs">🗑️</span>
              </button>
            </div>
          ))}
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-slate-700 min-w-[256px]">
          <button
            onClick={() => {
              onNewChat();
              if (window.innerWidth < 768) toggle();
            }}
            className="w-full bg-blue-600 py-2.5 rounded-lg font-semibold text-white hover:bg-blue-500 shadow-md transition-all active:scale-95"
          >
            + New Chat
          </button>
        </div>
      </div>
    </>
  );
};

export default Sidebar;