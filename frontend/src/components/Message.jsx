const Message = ({ role, content, isStreaming }) => (
  <div className={`mb-4 flex ${role === "user" ? "justify-end" : "justify-start"}`}>
    <div className={`max-w-[70%] px-4 py-2 rounded-xl ${
      role === "user"
        ? "bg-blue-600 text-white"
        : "bg-slate-100 text-slate-900"
    }`}>
      {content}
      {isStreaming && <span className="animate-pulse ml-1">▍</span>}
    </div>
  </div>
);

export default Message;
