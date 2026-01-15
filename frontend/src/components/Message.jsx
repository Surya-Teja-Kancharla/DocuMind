import React from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import clsx from "clsx";

const Message = ({ role, content, isStreaming = false }) => {
  const isUser = role === "user";

  return (
    <div
      className={clsx(
        "w-full flex mb-4",
        isUser ? "justify-end" : "justify-start"
      )}
    >
      <div
        className={clsx(
          "max-w-[70%] rounded-xl px-4 py-3 text-sm leading-relaxed",
          isUser
            ? "bg-blue-600 text-white"
            : "bg-slate-100 text-slate-900 dark:bg-slate-800 dark:text-slate-100"
        )}
      >
        <ReactMarkdown remarkPlugins={[remarkGfm]}>
          {content}
        </ReactMarkdown>

        {/* Streaming cursor */}
        {isStreaming && (
          <span className="inline-block ml-1 animate-pulse">▍</span>
        )}
      </div>
    </div>
  );
};

export default Message;
